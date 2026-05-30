# Supply Chain Mention Signal Rating SOP

**Version**: 1.0  
**Date**: 2026-05-29  
**Author**: D. Lee  
**Status**: Active  
**Project**: earnings-supply-signals v0.1

## Purpose

Define a consistent scoring framework for evaluating the signal quality of supply chain mentions extracted from earnings call documents. The goal is consistency across quarters and companies. Rate the strength of the evidence in the quote itself, not whether the quote sounds important overall.

## Scope

Applies to all mentions extracted by the LLM-based extractor pipeline in this project. Used for:

- Quality evaluation of prompt iterations
- Cross-transcript consistency analysis
- Future filtering of high-value mentions

## Inputs

For each extracted mention, review:

- `category`
- `speaker`
- `sentiment`
- `direct_quote`
- Surrounding transcript context (only when the quote is ambiguous)

## Output

Add a `"signal_strength"` field to each mention's JSON representation. Allowed values are only `"high"`, `"medium"`, or `"low"`.

Example:

```json
{
  "category": "supplier_relationship",
  "speaker": "CEO",
  "sentiment": "positive",
  "direct_quote": "we announced our EPIC co-development engagement with TSMC",
  "signal_strength": "high"
}
```

## Rating Rules & Definitions

### High Signal

Assign `high` when the quote contains at least one concrete, decision-useful detail.

**Indicators:**
- Specific supplier, partner, customer, university, or ecosystem participant name (e.g., SK Hynix, TSMC, Samsung, Micron)
- Quantitative data (e.g., specific number, dollar amount, percentage, capacity metric, or time horizon)
- Specific product, segment, node, device type, or end market
- Specific event (e.g., signed agreement, operational action, forecast, expansion, or capacity move)
- Evidence of customer behavior, supplier behavior, or committed planning

**Examples:**
- "equipment business will grow more than 30% this calendar year"
- "rolling eight-quarter forecasts"
- "EPIC co-development engagement with TSMC"
- "DRAM revenue of $1.7 billion grew 18% year-over-year"

### Medium Signal

Assign `medium` when the quote has substantive business content, but lacks specific evidence.

**Indicators:**
- Clear directional demand, supply, inventory, logistics, or readiness language
- Meaningful claim about operations or customer behavior
- No named counterparty, no concrete number, and no specific event
- Useful context, but not enough detail to stand alone as a strong signal

**Examples:**
- "we see strong demand from AI customers"
- "we are expanding our supply chain capabilities"
- "Customer pull-forward observed in advanced packaging"
- "customers are giving us longer visibility"

### Low Signal

Assign `low` when the quote is generic, promotional, or too vague to support an analytical conclusion.

**Indicators:**
- Boilerplate execution language
- Broad confidence statements without operational detail
- Generic PR language
- Claims that could apply to almost any company or quarter
- Mentions of supply chain with no clear action, actor, number, or business implication

**Examples:**
- "our supply chain is performing well"
- "strong operational execution"
- "we continue to execute our strategy"
- "Our team is delivering"

## Decision Workflow

1. **Read** the `direct_quote`.
2. **Check High:** Does the quote include a specific number, named entity, product segment, time horizon, agreement, or operational action? If **yes**, assign `high`.
3. **Check Medium:** If no, does the quote still provide a substantive supply-chain or demand signal? If **yes**, assign `medium`.
4. **Check Low:** If neither (e.g., mostly generic execution or PR language), assign `low`.

## Tie-Breaking Rules & Ambiguous Cases

- **Ambiguous cases**: When uncertain between two levels, default to the **lower** level (conservative scoring).
- Prefer `high` when a quote contains both generic language and one concrete detail.
- Prefer `medium` over `low` when the quote describes an actual business condition, even without numbers.
- Do not assign `high` only because the speaker is the CEO or CFO.
- Do not assign `high` only because sentiment is positive or negative.
- Do not penalize short quotes if they include a concrete signal.
- If the quote is duplicated across categories, use the same signal strength unless the category-specific interpretation changes the evidence quality.

## Category-Specific Guidance

| Category | High Signal Examples | Medium Signal Examples | Low Signal Examples |
| --- | --- | --- | --- |
| `demand_signal` | Growth percentages, revenue guidance, named product demand, customer forecasts | Strong demand, improved visibility, higher customer activity | Positive market commentary with no detail |
| `supply_constraint` | Full capacity, shortages, delayed deliveries, quantified capacity limits | Tight supply, constrained output, limited availability | General concern about supply environment |
| `inventory_position` | Dollar value, inventory increase/decrease, build plan, target level | Inventory strategy or positioning without numbers | Generic inventory discipline |
| `logistics_capacity` | Added logistics capacity, named logistics action, quantified capacity | Logistics readiness or capability expansion | Generic logistics execution |
| `supplier_relationship` | Named suppliers/partners, agreements, co-development, founder partners | Supplier visibility, supplier collaboration without names | Generic partner ecosystem language |
| `operational_readiness` | Capacity doubled, specific factory/service ramp, resource additions | Preparedness, readiness, output increase without details | Generic execution statement |

## QA Checklist

Before finalizing a rated JSON file:

- Every mention has exactly one `signal_strength`.
- Values are lowercase: `high`, `medium`, or `low`.
- Quotes with numbers or named entities were checked for `high`.
- Boilerplate execution quotes were checked for `low`.
- Similar quotes across transcripts (e.g., Q1 and Q2) use consistent ratings.
- The rating is based on evidence in the quote, not personal judgment about the company.