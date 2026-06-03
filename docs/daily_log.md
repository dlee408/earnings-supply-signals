# Project Daily Log

## Day 7 (2026-05-29) - H/M/L Evaluation

### Plan (morning)

- Phase 1 (5min): Reference signal_quality_sop_v1.md
- Phase 2 (47min): H/M/L tagging for Q2 v0.2 (20) + Q1 (17)
- Phase 3 (15min): Cross-transcript comparison table
- Phase 4 (30min): Decision + record
- Phase 5 (15min): Commit + push

### Results (evening)

- Q2 v0.2: H=15, M=4, L=1; High-signal rate = 15/20 = 75%
- Q1: H=10, M=5, L=2; High-signal rate = 10/17 = 58.8%
- Decision: Scenario A/B/C
  - Scenario A: >= 40% on both Q1 and Q2 --> v0.2 sufficient.Proceed to Day 8 (code modularization and refactor). 
- Issues encountered: [...]

### Day 7 Note: Cross-quarter signal density variance

Q2 FY26 (record quarter): 75% high-signal
Q1 FY26 (regular quarter): 58.8% high-signal

Variance reflects document content, not extraction inconsistency.
Record quarters contain more quantitative claims (revenue records,
growth percentages, named partner agreements).

Implication for v0.1: Extractor performance varies by transcript
character. Future versions may benefit from transcript-type tagging.

---

## Day 9 (2026-06-01) - temperature=0, project reframe, degree decision

### Phase 1: temperature=0 mitigation

Added `temperature=0` to `src/mention_extractor.py`.
Re-ran pipeline on Q1 + Q2 transcripts.

Baseline updated (with temperature=0):

- Q2 FY2026: 24 mentions (was 20 at temp=1 in Day 6)
- Q1 FY2026: 21 mentions (was 17 at temp=1 in Day 6)

Spot check finding:

- Day 6 mentions remain in new outputs (subset preserved)
- New mentions are mostly medium-low signal
- "neutral" sentiment value emerged (not previously seen)

Insight: temperature=0 increases comprehensiveness, not selectivity.
Trade-off documented for README.
...
