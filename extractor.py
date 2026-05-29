import json
import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

EXTRACTION_PROMPT = """You are analyzing an earnings call prepared remarks document from a semiconductor company. Extract all mentions related to supply chain.

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
{text}
---

Return the JSON array now."""


def extract_mentions(text: str) -> list:
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": EXTRACTION_PROMPT.format(text=text)}],
    )

    response_text = message.content[0].text.strip()

    # Parse JSON (may need to handle markdown code blocks)
    if response_text.startswith("```"):
        # Strip markdown code fence
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    return json.loads(response_text)


if __name__ == "__main__":
    text_path = Path("data") / "amat_q2_2026_clean.txt"
    output_path = Path("data") / "amat_q2_2026_mentions.json"

    text = text_path.read_text()
    print(f"Input text: {len(text)} chars, ~{len(text.split())} words")
    print("Calling Claude API...")

    mentions = extract_mentions(text)

    output_path.write_text(json.dumps(mentions, indent=2))

    print(f"---")
    print(f"Extracted {len(mentions)} mentions")
    print(f"Saved to {output_path}")
    print(f"---")
    print("Categories breakdown:")
    from collections import Counter

    cats = Counter(m["category"] for m in mentions)
    for cat, count in cats.most_common():
        print(f"  {cat}: {count}")
