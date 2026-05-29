import re
from pathlib import Path


def reconstruct_paragraphs(text: str) -> str:
    """
    pdfplumber extracts sentences on separate lines.
    True paragraph breaks should be double newlines (\n\n).
    Single \n between sentences -> replace with space.
    """

    # First, normalize multiple newlines to exactly two
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Then, single \n (not part of \n\n) -> space
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Clean up multiple spaces
    text = re.sub(r" {2,}", " ", text)

    return text


if __name__ == "__main__":
    input_path = Path("data") / "amat_q2_2026_extracted.txt"
    output_path = Path("data") / "amat_q2_2026_clean.txt"

    raw = input_path.read_text()
    clean = reconstruct_paragraphs(raw)
    output_path.write_text(clean)

    print(f"Input: {len(raw)} chars, {raw.count(chr(10))} newlines")
    print(f"Output: {len(clean)} chars, {clean.count(chr(10))} newlines")
    print(f"----")
    print("First 800 chars of cleaned text:")
    print(clean[:800])
