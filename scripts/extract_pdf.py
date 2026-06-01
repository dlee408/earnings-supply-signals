"""Reusable PDF text extraction helpers."""

import argparse
from dataclasses import dataclass
from pathlib import Path

import pdfplumber


@dataclass(frozen=True)
class PdfExtractionResult:
    """Text and basic diagnostics from a PDF extraction run."""

    text: str
    page_count: int
    page_char_counts: list[int]

    @property
    def char_count(self) -> int:
        return len(self.text)

    @property
    def word_count(self) -> int:
        return len(self.text.split())


def extract_pdf_text(
    pdf_path: str | Path,
    output_path: str | Path | None = None,
) -> PdfExtractionResult:
    """Extract text from a PDF and optionally save it to a text file.

    Args:
        pdf_path: Path to the source PDF.
        output_path: Optional path where extracted text should be written.

    Returns:
        A PdfExtractionResult containing the extracted text and page diagnostics.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    page_texts = []
    page_char_counts = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            page_texts.append(page_text)
            page_char_counts.append(len(page_text))

    full_text = "\n".join(page_texts)
    if full_text:
        full_text += "\n"

    if output_path is not None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(full_text, encoding="utf-8")

    return PdfExtractionResult(
        text=full_text,
        page_count=len(page_texts),
        page_char_counts=page_char_counts,
    )


def print_extraction_summary(
    result: PdfExtractionResult,
    output_path: str | Path | None = None,
    preview_chars: int = 500,
) -> None:
    """Print the same diagnostics used during exploratory PDF extraction."""
    print(f"Total pages: {result.page_count}")
    print("---")

    for page_index, char_count in enumerate(result.page_char_counts, start=1):
        print(f"Page {page_index}: {char_count} characters")

    print("---")
    print(f"Total characters: {result.char_count}")
    print(f"Estimated words: {result.word_count}")
    print("---")
    print(f"First {preview_chars} chars:")
    print("---")
    print(result.text[:preview_chars])
    print("---")
    print(f"Last {preview_chars} chars:")
    print("---")
    print(result.text[-preview_chars:])

    if output_path is not None:
        print(f"Saved extracted text to {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract plain text from a PDF file."
    )
    parser.add_argument(
        "pdf_path",
        type=Path,
        help="Path to the source PDF.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Optional path where extracted text should be saved.",
    )
    parser.add_argument(
        "--preview-chars",
        type=int,
        default=500,
        help="Number of characters to show from the start and end of the text.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    extraction = extract_pdf_text(args.pdf_path, args.output)
    print_extraction_summary(extraction, args.output, args.preview_chars)
