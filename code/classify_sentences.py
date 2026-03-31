"""
Classify FOMC sentences using Claude with Batches API + prompt caching.

Architecture:
    - System message (cached): Classification instructions, category definitions,
      few-shot examples (~1,200 tokens). Cached across all requests via
      cache_control: {"type": "ephemeral"} — cache reads cost 10% of base price.
    - User message: Just the numbered sentences (varies per request).
    - Batches API: 50% discount on all token types.
    - Run --estimate-cost to see detailed breakdown vs. base pricing.

Usage:
    # Estimate cost before running:
    python classify_sentences.py --estimate-cost

    # Pilot test on 200 random sentences (sequential, for prompt iteration):
    python classify_sentences.py --pilot --sample 200

    # Full batch classification (Batches API + prompt caching):
    python classify_sentences.py --batch

    # Check status / collect results from a running batch:
    python classify_sentences.py --collect BATCH_ID

    # Re-run low-confidence sentences:
    python classify_sentences.py --rerun-low-confidence
"""

import os
import re
import csv
import json
import sys
import time
import logging
import argparse
import random
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    DATA_DIR, PROMPTS_DIR, PILOT_DIR,
    ALL_SENTENCES_CSV, CLASSIFIED_SENTENCES_CSV, LOW_CONFIDENCE_CSV,
    MODEL_BULK, MODEL_QUALITY, MODEL_PILOT, MODEL_PI,
    BATCH_CHUNK_SIZE, SENTENCES_PER_REQUEST, MAX_TOKENS_PER_REQUEST,
    POLL_INTERVAL_SECONDS, TOPIC_CATEGORIES, CONFIDENCE_LEVELS,
)

try:
    import anthropic
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

MAX_RETRIES = 3


# ═══════════════════════════════════════════════════════════════════════════
# API Client
# ═══════════════════════════════════════════════════════════════════════════

def get_client():
    """Create Anthropic client."""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        logger.error("ANTHROPIC_API_KEY not set. Export it or set in config.py.")
        sys.exit(1)
    return anthropic.Anthropic(api_key=key)


def parse_json_response(text):
    """Parse LLM response text into JSON, stripping markdown fences."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)
    return json.loads(text)


# ═══════════════════════════════════════════════════════════════════════════
# Prompt Assembly
# ═══════════════════════════════════════════════════════════════════════════

def load_prompt_template(version="v2"):
    """Load the classification prompt template.

    Args:
        version: "v1" (original FS+FC split) or "v2" (merged FINANCIAL +
                 STABILITY_INTENSITY axis). Default is v2 — fixes the
                 conditional kappa=0.416 boundary problem in v1.
    """
    prompt_path = PROMPTS_DIR / f"classification_prompt_{version}.txt"
    if not prompt_path.exists():
        # Fall back to v1 if requested version is missing
        fallback = PROMPTS_DIR / "classification_prompt_v1.txt"
        logger.warning(f"Prompt {prompt_path.name} not found, falling back to v1")
        prompt_path = fallback
    if not prompt_path.exists():
        logger.error(f"Prompt template not found: {prompt_path}")
        sys.exit(1)
    logger.info(f"Using prompt: {prompt_path.name}")
    return prompt_path.read_text(encoding="utf-8")


def split_prompt_template(template):
    """Split prompt template into system instructions and output instructions.

    Returns (system_text, output_instruction):
        system_text: Classification instructions, definitions, examples
        output_instruction: The "Output a JSON array..." line
    The numbered sentences go in the user message at call time.
    """
    marker = "{NUMBERED_SENTENCES}"
    idx = template.index(marker)

    # Everything before "Sentences:\n{NUMBERED_SENTENCES}" is the system prompt
    pre = template[:idx].rstrip()
    if pre.endswith("Sentences:"):
        pre = pre[:-len("Sentences:")].rstrip()

    # Everything after the marker (e.g. "Output a JSON array of objects...")
    post = template[idx + len(marker):].strip()

    # Combine instructions + output format into system text
    system_text = pre
    if post:
        system_text = system_text + "\n\n" + post

    return system_text


def build_cached_system_blocks(system_text):
    """Build system message blocks with cache_control for prompt caching.

    Returns a list of content blocks suitable for the system= parameter.
    The cache_control on the last block tells the API to cache everything
    up to and including this block, saving ~90% on input tokens for
    subsequent requests with the same system prompt.
    """
    return [{
        "type": "text",
        "text": system_text,
        "cache_control": {"type": "ephemeral"},
    }]


def build_user_message(sentences):
    """Build user message containing only the numbered sentences.

    Args:
        sentences: List of (sentence_id, text) tuples
    Returns:
        String of numbered sentences for the user message.
    """
    return "\n".join(
        f"{i+1}. {text}" for i, (_, text) in enumerate(sentences)
    )


def build_prompt(template, sentences):
    """Build a single combined prompt (legacy, for debugging).

    Args:
        template: Prompt template with {NUMBERED_SENTENCES} placeholder
        sentences: List of (sentence_id, text) tuples
    """
    numbered = "\n".join(
        f"{i+1}. {text}" for i, (_, text) in enumerate(sentences)
    )
    return template.replace("{NUMBERED_SENTENCES}", numbered)


# ═══════════════════════════════════════════════════════════════════════════
# Sentence Loading
# ═══════════════════════════════════════════════════════════════════════════

def load_sentences(csv_path=None):
    """Load sentences from CSV. Returns list of dicts."""
    path = csv_path or ALL_SENTENCES_CSV
    with open(str(path), "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sample_pilot_sentences(sentences, n=200, seed=42):
    """Create a stratified sample for pilot testing.

    Samples proportionally from each doc_type, with oversampling of
    sentences containing Peek FI dictionary terms.
    """
    random.seed(seed)

    # Group by doc_type
    by_type = {}
    for s in sentences:
        dt = s.get("doc_type", "other")
        by_type.setdefault(dt, []).append(s)

    # Target proportions (roughly matching the plan)
    targets = {
        "transcript": int(n * 0.4),   # 80 sentences
        "minutes": int(n * 0.25),     # 50 sentences
        "statement": int(n * 0.15),   # 30 sentences
        "speech": int(n * 0.2),       # 40 sentences
    }

    sampled = []
    for dt, target_count in targets.items():
        pool = by_type.get(dt, [])
        if not pool:
            continue

        # Try to get ~30% of target from sentences with Peek FI terms
        fi_pool = [s for s in pool if s.get("peek_fi_binary", "0") == "1"]
        non_fi_pool = [s for s in pool if s.get("peek_fi_binary", "0") != "1"]

        fi_target = min(int(target_count * 0.3), len(fi_pool))
        non_fi_target = min(target_count - fi_target, len(non_fi_pool))

        sampled.extend(random.sample(fi_pool, fi_target) if fi_pool else [])
        sampled.extend(random.sample(non_fi_pool, non_fi_target) if non_fi_pool else [])

    random.shuffle(sampled)
    return sampled[:n]


# ═══════════════════════════════════════════════════════════════════════════
# Sequential Mode (Pilot Testing)
# ═══════════════════════════════════════════════════════════════════════════

def classify_sequential(sentences, model, client, system_blocks, batch_size=20):
    """Classify sentences sequentially (for pilot testing / debugging).

    Uses prompt caching: system_blocks contain the cached classification
    instructions, and only the numbered sentences are sent as user content.

    Returns list of classification results.
    """
    results = []
    total_batches = (len(sentences) + batch_size - 1) // batch_size
    cache_hits = 0
    total_input_tokens = 0
    total_cache_read_tokens = 0
    total_cache_creation_tokens = 0

    for batch_idx in range(0, len(sentences), batch_size):
        chunk = sentences[batch_idx:batch_idx + batch_size]
        batch_num = batch_idx // batch_size + 1

        # Build user message (just numbered sentences)
        sent_tuples = [(s["sentence_id"], s["text"]) for s in chunk]
        user_message = build_user_message(sent_tuples)

        logger.info(f"  Batch {batch_num}/{total_batches} ({len(chunk)} sentences)...")

        # Call API with retry
        for attempt in range(MAX_RETRIES):
            try:
                time.sleep(1.5)  # rate limit
                response = client.messages.create(
                    model=model,
                    max_tokens=MAX_TOKENS_PER_REQUEST,
                    system=system_blocks,
                    messages=[{"role": "user", "content": user_message}],
                )

                # Track cache usage
                usage = response.usage
                input_tok = getattr(usage, "input_tokens", 0)
                cache_read = getattr(usage, "cache_read_input_tokens", 0)
                cache_create = getattr(usage, "cache_creation_input_tokens", 0)
                total_input_tokens += input_tok
                total_cache_read_tokens += cache_read
                total_cache_creation_tokens += cache_create
                if cache_read > 0:
                    cache_hits += 1

                if batch_num <= 3 or batch_num % 10 == 0:
                    logger.info(
                        f"    Tokens: input={input_tok}, "
                        f"cache_read={cache_read}, cache_create={cache_create}"
                    )

                text = response.content[0].text
                classifications = parse_json_response(text)

                # Map results back to sentence IDs
                for i, cls in enumerate(classifications):
                    if i < len(chunk):
                        topic = cls.get("topic", "OTHER")
                        if topic not in TOPIC_CATEGORIES:
                            topic = "OTHER"
                        confidence = cls.get("confidence", "LOW")
                        if confidence not in CONFIDENCE_LEVELS:
                            confidence = "LOW"

                        results.append({
                            "sentence_id": chunk[i]["sentence_id"],
                            "topic": topic,
                            "confidence": confidence,
                            "reasoning": cls.get("reasoning", ""),
                        })
                break  # Success

            except json.JSONDecodeError as e:
                if attempt < MAX_RETRIES - 1:
                    logger.warning(f"JSON parse error (attempt {attempt+1}): {e}")
                    time.sleep(2)
                else:
                    logger.error(f"Failed to parse response for batch {batch_num}")
                    for s in chunk:
                        results.append({
                            "sentence_id": s["sentence_id"],
                            "topic": "ERROR",
                            "confidence": "LOW",
                            "reasoning": f"JSON parse error: {e}",
                        })
            except (anthropic.RateLimitError, anthropic.InternalServerError) as e:
                wait = (2 ** attempt) * 3
                logger.warning(f"API error (attempt {attempt+1}): {e}. Waiting {wait}s.")
                time.sleep(wait)
            except Exception as e:
                logger.error(f"Unexpected error in batch {batch_num}: {e}")
                for s in chunk:
                    results.append({
                        "sentence_id": s["sentence_id"],
                        "topic": "ERROR",
                        "confidence": "LOW",
                        "reasoning": f"Error: {e}",
                    })
                break

    # Report cache savings
    logger.info(f"Cache stats: {cache_hits}/{total_batches} batches had cache hits")
    logger.info(
        f"Token totals: input={total_input_tokens}, "
        f"cache_read={total_cache_read_tokens}, "
        f"cache_create={total_cache_creation_tokens}"
    )
    if total_cache_read_tokens > 0:
        pct = 100 * total_cache_read_tokens / (total_input_tokens + total_cache_read_tokens + total_cache_creation_tokens)
        logger.info(f"Cache read ratio: {pct:.1f}% of input tokens served from cache")

    return results


# ═══════════════════════════════════════════════════════════════════════════
# Batch Mode (Batches API — 50% cost savings)
# ═══════════════════════════════════════════════════════════════════════════

def prepare_batch_requests(sentences, model, system_blocks, batch_size=20):
    """Prepare Batches API requests with prompt caching.

    Each request uses the same cached system message (classification instructions)
    and a unique user message (numbered sentences). The Batches API caches the
    system prompt across requests, giving ~90% savings on input tokens on top of
    the 50% Batches discount.
    """
    requests = []

    for batch_idx in range(0, len(sentences), batch_size):
        chunk = sentences[batch_idx:batch_idx + batch_size]
        sent_tuples = [(s["sentence_id"], s["text"]) for s in chunk]
        user_message = build_user_message(sent_tuples)

        chunk_id = batch_idx // batch_size
        requests.append(Request(
            custom_id=f"chunk_{chunk_id:05d}",
            params=MessageCreateParamsNonStreaming(
                model=model,
                max_tokens=MAX_TOKENS_PER_REQUEST,
                system=system_blocks,
                messages=[{"role": "user", "content": user_message}],
            ),
        ))

    logger.info(f"Prepared {len(requests)} batch requests for {len(sentences)} sentences")
    logger.info(f"System prompt cached with cache_control: ephemeral")
    return requests


def submit_batch(client, requests, chunk_size=None):
    """Submit requests to the Batches API. Returns list of batch IDs."""
    if chunk_size is None:
        chunk_size = BATCH_CHUNK_SIZE

    batch_ids = []
    for start in range(0, len(requests), chunk_size):
        chunk = requests[start:start + chunk_size]
        chunk_num = start // chunk_size + 1
        total_chunks = (len(requests) + chunk_size - 1) // chunk_size
        logger.info(f"Submitting chunk {chunk_num}/{total_chunks} ({len(chunk)} requests)...")

        batch = client.messages.batches.create(requests=chunk)
        batch_ids.append(batch.id)
        logger.info(f"  Batch {batch.id} submitted (status: {batch.processing_status})")

    return batch_ids


def poll_batch(client, batch_id, poll_interval=None):
    """Poll batch until completion. Returns final batch object."""
    if poll_interval is None:
        poll_interval = POLL_INTERVAL_SECONDS

    logger.info(f"Polling batch {batch_id} every {poll_interval}s...")
    while True:
        batch = client.messages.batches.retrieve(batch_id)
        counts = batch.request_counts
        logger.info(
            f"  Status: {batch.processing_status} | "
            f"processing={counts.processing}, succeeded={counts.succeeded}, "
            f"errored={counts.errored}, expired={counts.expired}"
        )
        if batch.processing_status == "ended":
            return batch
        time.sleep(poll_interval)


def collect_batch_results(client, batch_id, sentences, batch_size=20):
    """Collect results from a completed batch and map back to sentence IDs.

    Returns list of classification result dicts.
    """
    results = []
    succeeded = 0
    errored = 0

    # Build chunk_id → sentence list mapping
    chunk_map = {}
    for batch_idx in range(0, len(sentences), batch_size):
        chunk_id = batch_idx // batch_size
        chunk_map[f"chunk_{chunk_id:05d}"] = sentences[batch_idx:batch_idx + batch_size]

    for result in client.messages.batches.results(batch_id):
        custom_id = result.custom_id
        chunk_sentences = chunk_map.get(custom_id, [])

        if result.result.type == "succeeded":
            succeeded += 1
            text = result.result.message.content[0].text
            try:
                classifications = parse_json_response(text)
                for i, cls in enumerate(classifications):
                    if i < len(chunk_sentences):
                        topic = cls.get("topic", "OTHER")
                        if topic not in TOPIC_CATEGORIES:
                            topic = "OTHER"
                        confidence = cls.get("confidence", "LOW")
                        if confidence not in CONFIDENCE_LEVELS:
                            confidence = "LOW"

                        results.append({
                            "sentence_id": chunk_sentences[i]["sentence_id"],
                            "topic": topic,
                            "confidence": confidence,
                            "reasoning": cls.get("reasoning", ""),
                        })
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parse error for {custom_id}: {e}")
                for s in chunk_sentences:
                    results.append({
                        "sentence_id": s["sentence_id"],
                        "topic": "ERROR",
                        "confidence": "LOW",
                        "reasoning": f"JSON parse error: {e}",
                    })

        elif result.result.type == "errored":
            errored += 1
            logger.warning(f"Error for {custom_id}: {result.result.error}")
            for s in chunk_sentences:
                results.append({
                    "sentence_id": s["sentence_id"],
                    "topic": "ERROR",
                    "confidence": "LOW",
                    "reasoning": "API error",
                })

        elif result.result.type == "expired":
            errored += 1
            logger.warning(f"Expired: {custom_id}")

    logger.info(f"Collected: {succeeded} succeeded, {errored} errored")
    return results


# ═══════════════════════════════════════════════════════════════════════════
# Output Writing
# ═══════════════════════════════════════════════════════════════════════════

def merge_classifications(sentences, classifications, output_path):
    """Merge classification results into the sentence data and write CSV."""
    # Build lookup: sentence_id → classification
    cls_map = {}
    for c in classifications:
        cls_map[c["sentence_id"]] = c

    # Merge
    fieldnames = list(sentences[0].keys()) + ["topic", "confidence", "reasoning"]
    # Deduplicate fieldnames
    seen = set()
    unique_fieldnames = []
    for fn in fieldnames:
        if fn not in seen:
            unique_fieldnames.append(fn)
            seen.add(fn)
    fieldnames = unique_fieldnames

    merged = []
    for sent in sentences:
        row = dict(sent)
        cls = cls_map.get(sent["sentence_id"], {})
        row["topic"] = cls.get("topic", "")
        row["confidence"] = cls.get("confidence", "")
        row["reasoning"] = cls.get("reasoning", "")
        merged.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(output_path), "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged)

    # Stats
    topic_counts = {}
    low_conf = 0
    errors = 0
    for row in merged:
        t = row.get("topic", "")
        topic_counts[t] = topic_counts.get(t, 0) + 1
        if row.get("confidence") == "LOW":
            low_conf += 1
        if t == "ERROR":
            errors += 1

    logger.info(f"Wrote {len(merged)} classified sentences to {output_path}")
    logger.info("Topic distribution:")
    for t, c in sorted(topic_counts.items()):
        logger.info(f"  {t:25s}: {c:6d} ({100*c/len(merged):.1f}%)")
    logger.info(f"Low confidence: {low_conf} ({100*low_conf/len(merged):.1f}%)")
    if errors:
        logger.warning(f"Errors: {errors}")

    # Write low-confidence sentences for review
    low_conf_rows = [r for r in merged if r.get("confidence") == "LOW"]
    if low_conf_rows:
        with open(str(LOW_CONFIDENCE_CSV), "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(low_conf_rows)
        logger.info(f"Wrote {len(low_conf_rows)} low-confidence sentences to {LOW_CONFIDENCE_CSV}")

    return merged


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def estimate_cost(sentences, model, batch_size=20, batches_api=True):
    """Estimate API cost for classification run using actual sentence data.

    Pricing (per million tokens, verified Feb 2026 from platform.claude.com):
        Sonnet 4.6: input=$3, output=$15, cache_read=$0.30, cache_write=$3.75
        Haiku 4.5:  input=$1, output=$5,  cache_read=$0.10, cache_write=$1.25
        Batches API: 50% off all token types (stacks with caching discounts)
    """
    pricing = {
        "claude-opus-4-6": {
            "input": 15.0, "output": 75.0, "cache_read": 1.50, "cache_write": 18.75,
        },
        "claude-sonnet-4-6": {
            "input": 3.0, "output": 15.0, "cache_read": 0.30, "cache_write": 3.75,
        },
        "claude-haiku-4-5-20251001": {
            "input": 1.0, "output": 5.0, "cache_read": 0.10, "cache_write": 1.25,
        },
    }
    p = pricing.get(model, pricing["claude-sonnet-4-6"])
    batch_discount = 0.5 if batches_api else 1.0
    n_sentences = len(sentences)

    n_requests = (n_sentences + batch_size - 1) // batch_size

    # System prompt tokens: actual character count / ~3.5 chars per token
    template = load_prompt_template()
    system_text = split_prompt_template(template)
    sys_tokens = int(len(system_text) / 3.5)

    # User message tokens: compute from actual sentence word counts
    # ~1.3 tokens per word + ~3 tokens numbering overhead per sentence
    word_counts = [int(s.get("word_count", 25)) for s in sentences]
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 25
    tokens_per_sentence = avg_words * 1.3 + 3  # numbering prefix "1. "
    user_tokens_per_req = int(tokens_per_sentence * batch_size)

    # Output tokens: JSON object per sentence
    # {"id":1,"topic":"FINANCIAL_STABILITY","confidence":"HIGH","reasoning":"..."}
    # ~40 tokens per entry + array overhead
    output_per_sentence = 40
    output_tokens_per_req = output_per_sentence * batch_size + 20  # array brackets

    # ─── Scenario 1: Batches + caching (our approach) ───
    cache_write_cost = (sys_tokens / 1e6) * p["cache_write"] * batch_discount
    cache_read_cost = ((n_requests - 1) * sys_tokens / 1e6) * p["cache_read"] * batch_discount
    input_cost = (n_requests * user_tokens_per_req / 1e6) * p["input"] * batch_discount
    output_cost = (n_requests * output_tokens_per_req / 1e6) * p["output"] * batch_discount
    total = cache_write_cost + cache_read_cost + input_cost + output_cost

    # ─── Scenario 2: Batches only (no caching) ───
    batches_only_input = (n_requests * (sys_tokens + user_tokens_per_req) / 1e6) * p["input"] * batch_discount
    batches_only_total = batches_only_input + output_cost

    # ─── Scenario 3: No discounts at all (baseline) ───
    base_input = (n_requests * (sys_tokens + user_tokens_per_req) / 1e6) * p["input"]
    base_output = (n_requests * output_tokens_per_req / 1e6) * p["output"]
    base_total = base_input + base_output

    total_input_tokens = n_requests * (sys_tokens + user_tokens_per_req)
    total_output_tokens = n_requests * output_tokens_per_req

    logger.info(f"")
    logger.info(f"Cost estimate for {model}:")
    logger.info(f"  Sentences: {n_sentences:,} -> {n_requests:,} API requests ({batch_size}/req)")
    logger.info(f"  Avg words/sentence: {avg_words:.0f} -> ~{tokens_per_sentence:.0f} tokens/sentence")
    logger.info(f"  System prompt: {sys_tokens:,} tokens (cached)")
    logger.info(f"  Per request: ~{user_tokens_per_req:,} input + ~{output_tokens_per_req:,} output tokens")
    logger.info(f"  Total tokens: ~{total_input_tokens:,} input + ~{total_output_tokens:,} output")
    logger.info(f"")
    logger.info(f"  {'Scenario':<30s} {'Input':>8s} {'Output':>8s} {'Total':>8s}")
    logger.info(f"  {'-'*56}")
    logger.info(f"  {'Base (no discounts)':<30s} ${base_input:>7.2f} ${base_output:>7.2f} ${base_total:>7.2f}")
    logger.info(f"  {'Batches only (50% off)':<30s} ${batches_only_input:>7.2f} ${output_cost:>7.2f} ${batches_only_total:>7.2f}")
    logger.info(
        f"  {'Batches + caching (ours)':<30s} "
        f"${cache_write_cost + cache_read_cost + input_cost:>7.2f} "
        f"${output_cost:>7.2f} ${total:>7.2f}"
    )
    logger.info(f"")
    logger.info(f"  Savings vs base: ${base_total - total:.2f} ({100*(1 - total/base_total):.0f}%)")

    return total


def main():
    parser = argparse.ArgumentParser(description="Classify FOMC sentences with LLM")
    parser.add_argument("--pilot", action="store_true",
                        help="Run pilot test on a sample (sequential mode)")
    parser.add_argument("--pi-labels", action="store_true",
                        help="Generate PI gold-standard labels using Opus 4.6 (batch_size=5)")
    parser.add_argument("--sample", type=int, default=200,
                        help="Number of sentences to sample for pilot (default: 200)")
    parser.add_argument("--batch", action="store_true",
                        help="Run full classification using Batches API")
    parser.add_argument("--collect", type=str, default=None,
                        help="Collect results from a completed batch ID")
    parser.add_argument("--rerun-low-confidence", action="store_true",
                        help="Re-classify low-confidence sentences with quality model")
    parser.add_argument("--model", type=str, default=None,
                        help="Override model (default: depends on mode)")
    parser.add_argument("--input", type=str, default=None,
                        help="Input CSV path (default: all_sentences.csv)")
    parser.add_argument("--output", type=str, default=None,
                        help="Output CSV path")
    parser.add_argument("--batch-size", type=int, default=SENTENCES_PER_REQUEST,
                        help="Sentences per API request (default: 20)")
    parser.add_argument("--estimate-cost", action="store_true",
                        help="Estimate cost without running classification")
    parser.add_argument("--prompt-version", type=str, default="v2",
                        choices=["v1", "v2"],
                        help="Prompt version: v2 (default, merged FINANCIAL+STABILITY_INTENSITY) "
                             "or v1 (original FS/FC split, conditional kappa=0.416)")
    args = parser.parse_args()

    # Load and split prompt template into system (cached) + user parts
    template = load_prompt_template(version=args.prompt_version)
    system_text = split_prompt_template(template)
    system_blocks = build_cached_system_blocks(system_text)
    logger.info(f"System prompt: {len(system_text)} chars (will be cached across requests)")

    # Determine input
    input_path = args.input or str(ALL_SENTENCES_CSV)
    # Use scored file if available
    scored_path = DATA_DIR / "all_sentences_scored.csv"
    if not args.input and scored_path.exists():
        input_path = str(scored_path)

    sentences = load_sentences(input_path)
    logger.info(f"Loaded {len(sentences)} sentences from {input_path}")

    if args.estimate_cost:
        # Just estimate cost and exit
        model = args.model or MODEL_BULK
        estimate_cost(sentences, model, args.batch_size, batches_api=True)
        return

    client = get_client()

    if args.pi_labels:
        # PI gold-standard labeling with Opus 4.6
        model = args.model or MODEL_PI
        pi_batch_size = min(args.batch_size, 5)  # smaller batches for max quality
        sample = sample_pilot_sentences(sentences, args.sample)

        # Save the sample for later Sonnet pilot comparison
        sample_path = PILOT_DIR / "pilot_sample_200.csv"
        PILOT_DIR.mkdir(parents=True, exist_ok=True)
        with open(str(sample_path), "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(sample[0].keys()))
            writer.writeheader()
            writer.writerows(sample)
        logger.info(f"Saved {len(sample)}-sentence sample to {sample_path}")

        logger.info(f"PI labeling: {len(sample)} sentences with {model} (batch_size={pi_batch_size})")
        estimate_cost(sample, model, pi_batch_size, batches_api=False)

        classifications = classify_sequential(
            sample, model, client, system_blocks, pi_batch_size
        )

        output_path = Path(args.output) if args.output else (PILOT_DIR / "pi_labels_200.csv")
        merge_classifications(sample, classifications, output_path)

        # Print summary statistics
        from collections import Counter
        topic_counts = Counter(c["topic"] for c in classifications)
        conf_counts = Counter(c["confidence"] for c in classifications)
        logger.info(f"\n{'='*60}")
        logger.info(f"PI Label Summary ({model}):")
        logger.info(f"  Topics: {dict(sorted(topic_counts.items()))}")
        logger.info(f"  Confidence: {dict(sorted(conf_counts.items()))}")
        fi_sample = sum(1 for s in sample if s.get("peek_fi_binary", "0") == "1")
        logger.info(f"  Peek FI sentences in sample: {fi_sample}/{len(sample)}")
        logger.info(f"{'='*60}")

    elif args.pilot:
        # Pilot mode: sample and classify sequentially
        model = args.model or MODEL_PILOT
        sample = sample_pilot_sentences(sentences, args.sample)
        logger.info(f"Pilot test: {len(sample)} sentences with {model}")
        estimate_cost(sample, model, args.batch_size, batches_api=False)

        classifications = classify_sequential(
            sample, model, client, system_blocks, args.batch_size
        )

        output_path = Path(args.output) if args.output else (PILOT_DIR / "pilot_results.csv")
        merge_classifications(sample, classifications, output_path)

    elif args.collect:
        # Collect results from a previously submitted batch
        logger.info(f"Collecting results from batch {args.collect}")
        classifications = collect_batch_results(
            client, args.collect, sentences, args.batch_size
        )
        output_path = Path(args.output) if args.output else CLASSIFIED_SENTENCES_CSV
        merge_classifications(sentences, classifications, output_path)

    elif args.batch:
        # Full batch mode with prompt caching
        model = args.model or MODEL_BULK
        logger.info(f"Full batch classification: {len(sentences)} sentences with {model}")
        logger.info(f"Using Batches API (50% discount) + prompt caching (~90% input savings)")
        estimate_cost(sentences, model, args.batch_size, batches_api=True)

        requests = prepare_batch_requests(
            sentences, model, system_blocks, args.batch_size
        )

        batch_ids = submit_batch(client, requests)

        # Save batch IDs for later collection
        batch_info = {
            "batch_ids": batch_ids,
            "model": model,
            "total_sentences": len(sentences),
            "batch_size": args.batch_size,
            "prompt_caching": True,
            "submitted_at": datetime.now().isoformat(),
        }
        info_path = DATA_DIR / "batch_info.json"
        info_path.write_text(json.dumps(batch_info, indent=2), encoding="utf-8")
        logger.info(f"Batch info saved to {info_path}")

        # Poll and collect
        for bid in batch_ids:
            poll_batch(client, bid)

        all_classifications = []
        for bid in batch_ids:
            results = collect_batch_results(client, bid, sentences, args.batch_size)
            all_classifications.extend(results)

        output_path = Path(args.output) if args.output else CLASSIFIED_SENTENCES_CSV
        merge_classifications(sentences, all_classifications, output_path)

    elif args.rerun_low_confidence:
        # Re-run low-confidence sentences with higher-quality model
        model = args.model or MODEL_QUALITY
        low_conf_path = LOW_CONFIDENCE_CSV
        if not low_conf_path.exists():
            logger.error(f"No low-confidence file found at {low_conf_path}")
            sys.exit(1)

        low_conf = load_sentences(str(low_conf_path))
        logger.info(f"Re-classifying {len(low_conf)} low-confidence sentences with {model}")
        estimate_cost(low_conf, model, args.batch_size, batches_api=False)

        classifications = classify_sequential(
            low_conf, model, client, system_blocks, args.batch_size
        )

        output_path = Path(args.output) if args.output else (DATA_DIR / "reclassified_low_conf.csv")
        merge_classifications(low_conf, classifications, output_path)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
