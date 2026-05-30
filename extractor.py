"""Extract supply chain mentions from earnings call transcripts using Claude API."""

import json
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from collections import Counter

load_dotenv()
client = Anthropic()

PROMPT_VERSION = "0.2"

EXTRACTION_PROMPT = (
    """You are analyzing an earnings call prepared remarks document from a
    semiconductor company. Extract all mentions related to supply chain.

For each mention, classify it into one of these categories:
- supply_constraint: supply shortage, capacity limits, delayed deliveries,
  supplier or factory capacity issues
- demand_signal: customer demand changes, order momentum, forward guidance,
  product-specific demand drivers
- inventory_position: inventory levels, stocking strategy, build plan and
  inventory balance
- logistics_capacity: transportation, warehousing, and logistics operations
- supplier_relationship: supplier partnerships, vendor dependencies,
  co-development partners, named collaboration relationships
- operational_readiness: supply chain operational preparedness and readiness

Use these rules:
- If the text describes stronger customer orders, incremental requests, or
  expected revenue growth, classify it as demand_signal.
- If the text describes limited supply, production constraints, or capacity
  shortages, classify it as supply_constraint.
- If the text describes inventory on hand, inventory strategy, or inventory
  build plans, classify it as inventory_position.
- If the text describes named partners, joint development, or founder-partner
  collaborations, classify it as supplier_relationship.
- For product-level demand signals, include examples such as foundry-logic,
  DRAM, advanced packaging, NAND, semiconductor equipment, and Applied's
  EPIC platform growth.

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
{text}
---

Return the JSON array now."""
)


def extract_mentions(input_text: str) -> list:
    """Extract supply chain mentions from text using Claude.

    Args:
        input_text: The earnings call transcript text to analyze.

    Returns:
        A list of extracted mentions with categories, speakers, sentiment, and quotes.
    """
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": EXTRACTION_PROMPT.format(text=input_text)}
        ],
    )

    # Extract text from content block
    text_block = None
    for block in message.content:
        text_attr = getattr(block, "text", None)
        if text_attr is not None:
            text_block = block
            break
    if text_block is None:
        raise ValueError("No text block in response")
    response_text = getattr(text_block, "text").strip()

    # Parse JSON (may need to handle markdown code blocks)
    if response_text.startswith("```"):
        # Strip markdown code fence
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    return json.loads(response_text)


if __name__ == "__main__":
    text_path = Path("data") / "amat_q1_2026_clean.txt"
    output_path = Path("data") / f"amat_q1_2026_mentions_v{PROMPT_VERSION}.json"

    transcript = text_path.read_text()
    print(f"Input text: {len(transcript)} chars, ~{len(transcript.split())} words")
    print("Calling Claude API...")

    mentions = extract_mentions(transcript)

    output_path.write_text(json.dumps(mentions, indent=2))

    print("---")
    print(f"Extracted {len(mentions)} mentions")
    print(f"Saved to {output_path}")
    print("---")
    print("Categories breakdown:")

    cats = Counter(m["category"] for m in mentions)
    for cat, count in cats.most_common():
        print(f"  {cat}: {count}")
