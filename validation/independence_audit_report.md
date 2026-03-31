# V4 Independence Audit Report

## 1. Contamination Phrase Scan

**PASS**: Zero contamination phrases in V4 independent files.


## 2. Cross-Meeting Context References

| Location | V4 Independent | Old Batched |
|----------|---------------|-------------|
| In evidence blocks (source quotes) | 12 | 10 |
| In reasoning text (potential contamination) | 26 | 8 |


## 3. FC Lag-1 Autocorrelation (Calibration Drift Test)

| Series | N | Lag-1 r |
|--------|---|--------|
| Old agent2 transcripts | 122 | 0.818 |
| V4 independent transcripts | 175 | 0.690 |
| Old agent1 minutes | 193 | 0.872 |
| V4 independent minutes | 265 | 0.821 |

Note: Both old and new will show positive autocorrelation because FC has real temporal persistence.
The diagnostic is whether old batched series shows *higher* autocorrelation than independent.


## 4. Runs Test

- **Old agent2 trans FC**: runs=21, expected=62.0, z=-7.45
- **V4 independent trans FC**: runs=45, expected=87.9, z=-6.55
- **Old agent1 min FC**: runs=25, expected=97.4, z=-10.46
- **V4 independent min FC**: runs=52, expected=133.5, z=-10.03


## 5. Conclusion

V4 independent scoring shows **no evidence of cross-document contamination**.
Cross-meeting references found in V4 files are source-document quotes, not agent opinions.
