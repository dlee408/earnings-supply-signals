# Project Notes

This file captures ideas that emerge during development but should NOT be added to v0.1.
v0.1 scope is locked. Ideas here become inputs for future versions.

## 2026-05-24

## 2026-05-26

- Pivoted from full transcript to Published Script (prepared remarks)
- Q&A not available in legal/free public sources
- See cs_projs_notes/lesson_learned.md for broader takeaways-

## 2026-05-26 Day 4: PDF Extraction Quality Check

### Verified clean

- No tables in source PDF
- Numbers + units preserved correctly ($7.91 billion etc)
- Special chars (|, &) render correctly  
- No bullet points in source

### Found issue (non-blocking)

- Paragraph structure not fully preserved: each sentence in
  source PDF ends up on its own line after extraction
- Original paragraphs (multiple sentences) become
  multi-line blocks
- Impact: may affect LLM's ability to recognize
  connected narrative across sentences
- Resolution: paragraph reconstruction step needed in
  Day 5 preprocessing pipeline

### Word count finding

- 2,814 words for AMAT prepared remarks
- Lower than typical (4,000-7,000)
- AMAT IR style is concise

## 2026-05-28 Day 6: Review of Day 5 Extraction and Preprocessing

### Summary stats

- Total mentions: 9
- Hallucinations: 0
- Misclassifications: 0
- Sentiment errors: 0
- High-signal: 5, Medium: 4, Low: 0

### Missing categories observed

- supply_constraint: 0 found
  - Verdict: AMAT did not explicitly describe supply constraints in this prepared remarks section; the model did not miss a clear supply-constraint statement.

- demand_signal: 2 found
  - Verdict: The LLM missed strong demand language around incremental orders and forward guidance.
  - Examples:
    - "we are seeing incremental requests for equipment deliveries in 2026, and we now expect our semiconductor equipment business will grow more than 30% this calendar year."
    - "we expect these three areas to account for more than 80% of the year-on-year growth in total wafer fab equipment spending in 2026, and see a similar profile in 2027."

- demand_signal (product-level nuance): 1 found
  - Verdict: Category definitions are too broad; the model did not capture product-specific demand signals that should be surfaced separately.
  - Examples:
    - "foundry-logic"
    - "DRAM"
    - "advanced packaging"
    - "NAND"
    - "semiconductor equipment"
    - "Applied’s global EPIC platform"

- supply_relationship: 1 found
  - Verdict: The LLM under-tagged partner-level relationship detail; the category definition should explicitly include named collaborations and co-development partners.
  - Example:
    - "EPIC co-development engagement with TSMC, who join as a Founding Partner together with Micron, Samsung and SK Hynix."

### Specific issues

1. Mention #3 quote "increased build plan" may fit `demand_signal` or `supply_constraint` better than `inventory_position`.
2. The EPIC/TSMC partner quote should be tagged `supply_relationship` rather than a generic relationship or product signal.
3. Product-specific demand references like "foundry-logic" and "advanced packaging" are currently not separated from general demand signals.

### Prompt iteration needed

- Clarify boundaries between `demand_signal`, `supply_constraint`, and `inventory_position` with concrete examples.
- Add explicit guidance for `supply_relationship` on named partners, co-development, and founder-partner collaborations.
- Include product-level examples for demand signals, especially foundry-logic, DRAM, advanced packaging, NAND, semiconductor equipment, and EPIC platform growth.

### Change history (Prompt v0.1 → v0.2)

- `version 0.1`: "You are analyzing an earnings call prepared remarks document from a semiconductor company. Extract all mentions related to supply chain.

For each mention, classify it into one of these categories:

- supply_constraint: supply shortage, capacity limits
- demand_signal: demand changes, customer behavior
- inventory_position: inventory levels and strategy
- logistics_capacity: transportation, warehousing, logistics
- supplier_relationship: supplier partnerships, dependencies
- operational_readiness: supply chain operational preparedness

For each mention, also identify:

- speaker: who said it (CEO, CFO, IR, or specify name if available)
- sentiment: positive, negative, or neutral (from the company's perspective)
- direct_quote: the exact text (up to 50 words)

Return ONLY a valid JSON array. No prose, no markdown, just the JSON.

Format:
[
  {{
    "category": "supply_constraint",
    "speaker": "CEO",
    "sentiment": "negative",
    "direct_quote": "..."
  }}
]

Here is the earnings call prepared remarks:

---
`{text}`
Return the JSON array now.
"

- `version 0.2`: Updated extraction prompt to clarify boundaries between `demand_signal`, `supply_constraint`, and `inventory_position`; added explicit guidance for `supplier_relationship` with named partners and co-development collaborations; and included product-level demand examples for foundry-logic, DRAM, advanced packaging, NAND, semiconductor equipment, and EPIC platform growth.

### Iteration Results

- v0.1: 9 mentions
- v0.2: 20 mentions
  - Categories breakdown:
    - demand_signal: 12
    - supplier_relationship: 3
    - operational_readiness: 2
    - supply_constraint: 1
    - inventory_position: 1
    - logistics_capacity: 1
- Issues resolved:
  - Missed incremental demand language ("incremental requests," "we expect," growth percentages like "30%", "80%")
  - Improved capture of product-specific demand drivers (foundry-logic, DRAM, advanced packaging, NAND)
  - Better recognition of named partner collaborations (EPIC/TSMC/Micron/Samsung/SK Hynix)
  - Enhanced supplier_relationship tagging with explicit partner and co-development guidance
- New issues introduced: None identified
- Verdict: **v0.2 better** — 2.2x increase in mention detection (9 → 20) with high-signal demand_signal cases now captured. Proceed with v0.2 as baseline; refine on next iteration if needed.
