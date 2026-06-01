"""PDF text extraction from earnings call documents."""

from pathlib import Path
import pdfplumber


def extract_text_from_pdf(pdf_path: Path) -> tuple[str, int]:
    """
    Extract test from a PDF file

    Returns:
        (full_text, num_pages)
    """
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = []
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages_text.append(text)
        full_text = "\n".join(pages_text)
        return full_text, len(pdf.pages)


def save_extracted_text(text: str, output_path: Path) -> None:
    """Save extracted text to a file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text)


if __name__ == "__main__":
    # Standalone usage
    import sys

    pdf_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    text, pages = extract_text_from_pdf(pdf_path)
    save_extracted_text(text, output_path)

    print(f"Extracted {pages} pages, {len(text.split())} words")
    print(f"Saved to {output_path}")
