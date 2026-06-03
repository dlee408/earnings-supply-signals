"""LLM-based supply chain mention extraction."""

import json
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
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


def extract_mention(text: str, model: str = "claude-sonnet-4-5") -> list[dict]:
    """
    Extract supply chain mentions from earnings call text using Claude.

    Return:
        List of mention dicts with keys: category, speaker, sentiment, direct_quote
    """
    client = Anthropic()

    message = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=0,  # try to fix variance between LLM API call
        messages=[
            {
                "role": "user",
                "content": EXTRACTION_PROMPT.format(text=text),
            }
        ],
    )

    response_text = message.content[0].text.strip()

    # Strip markdonw code fence if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    return json.loads(response_text)


def extract_from_file(input_path: Path, output_path: Path) -> int:
    """Extract mentions from a cleaned text file, save JSON output."""
    text = input_path.read_text()
    mentions = extract_mention(text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(mentions, indent=2))

    return len(mentions)


if __name__ == "__main__":
    import sys

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    print(f"Extracting mentions from {input_path}...")
    count = extract_from_file(input_path, output_path)
    print(f"Extracted {count} mentions -> {output_path}")
