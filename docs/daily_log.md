# Project Daily Log

## Day 7 - H/M/L Evaluation

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

## Day 9 - temperature=0, project reframe, degree decision

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

## Day 9 (2026-06-01) - v0.1 SHIPPED

### Substantive work today

**Phase 1: temperature=0 baseline**

- Added `temperature=0` to mention_extractor.py
- New baseline: Q2 FY2026 = 24 mentions, Q1 FY2026 = 21 mentions
- Variance analysis: temperature=0 increases comprehensiveness not selectivity
- "neutral" sentiment value emerged (acceptable schema extension)

**Phase 2: Major decisions**

- Project reframe: "honest learning project" not "production tool"

**Phase 3: README + example**

- README v1.0: 136 lines, all sections
- Theory of Constraints framing for "What this demonstrates"
- Mermaid pipeline diagram in "How it works"
- 5 honest limitations documented
- 1 example case study: AMAT Q2 FY2026 record quarter

### Total session time

~5 hours across morning, afternoon

### v0.1 deliverables shipped

- ✓ End-to-end pipeline (PDF → JSON)
- ✓ 4 modules in src/
- ✓ SOP document (signal_quality_sop_v1.md)
- ✓ README v1.0
- ✓ 1 example case study
- ✓ Daily log (9 entries)
- ✓ All on public GitHub

### Outstanding items (intentionally deferred)

- Post draft → in plan
- Examples beyond 1 → out of v0.1 scope
- Error handling, logging → out of v0.1 scope
- Q&A transcript processing → out of v0.1 scope, future v0.2 candidate

### Status: v0.1 SHIPPED
