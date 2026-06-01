"""Text preprocessing for earnings call documents."""

import re
from pathlib import Path


def reconstruct_paragraphs(text: str) -> str:
    """
    Convert pdfplumber's line-persentence output back to paragraphs.

    pdfplumber outputs each sentence on a new line. True paragraph breaks
    appear as double newlines. This function:
     - Preserves paragraph breaks (\\n\\n)
     - Joins sentence-level breaks (\\n) with spaces
     - Normalizes multiple spaces
    """
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    text = re.sub(r" {2,}", " ", text)
    return text


def preprocess_file(input_path: Path, output_path: Path) -> None:
    """Read raw text, reconstruct paragraphs, write to output."""
    raw = input_path.read_text()
    clean = reconstruct_paragraphs(raw)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(clean)


if __name__ == "__main__":
    import sys

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    preprocess_file(input_path, output_path)
    print(f"Preprocessed {input_path} -> {output_path}")
