"""End-to-end pipeline: PDF -> mentions JSON."""

import difflib
from pathlib import Path

from src.pdf_extractor import extract_text_from_pdf, save_extracted_text
from src.preprocessor import preprocess_file
from src.mention_extractor import extract_from_file


def resolve_pdf_path(pdf_path: Path) -> Path:
    """Resolve common CLI path typos before opening the PDF."""
    if pdf_path.exists():
        return pdf_path

    parent = pdf_path.parent if pdf_path.parent != Path("") else Path(".")
    available_pdfs = list(parent.glob("*.pdf")) if parent.exists() else []

    candidates = [pdf_path]
    if pdf_path.name.endswith(".pdf Script.pdf"):
        candidates.append(pdf_path.with_name(pdf_path.name.removesuffix(" Script.pdf")))

    for candidate in candidates:
        if candidate.exists():
            return candidate

        for available_pdf in available_pdfs:
            if available_pdf.name.casefold() == candidate.name.casefold():
                return available_pdf

    suggestions = difflib.get_close_matches(
        pdf_path.name,
        [available_pdf.name for available_pdf in available_pdfs],
        n=3,
        cutoff=0.45,
    )
    message = f"PDF not found: {pdf_path}"
    if suggestions:
        message += "\nDid you mean one of these?\n" + "\n".join(
            f"  {parent / suggestion}" for suggestion in suggestions
        )
    raise FileNotFoundError(message)


def process_pdf(pdf_path: Path, output_dir: Path, name: str) -> dict:
    """
    Run the full pipeline on a PDF.

    Args:
      pdf_path: Path to the source PDF
      output_dir: Where to put intermediate and final outputs
      name: name for output files (e.g., "amat_q2_2026")

    Returns:
      Dict with file paths and counts
    """
    extracted_path = output_dir / f"{name}_extracted.txt"
    clean_path = output_dir / f"{name}_clean.txt"
    mentions_path = output_dir / f"{name}_mentions.json"

    # Step 1: PDF -> text
    pdf_path = resolve_pdf_path(pdf_path)
    text, pages = extract_text_from_pdf(pdf_path)
    save_extracted_text(text, extracted_path)

    # Step 2: Text -> clean text
    preprocess_file(extracted_path, clean_path)

    # Step 3: Clean text --> mentions
    count = extract_from_file(clean_path, mentions_path)

    return {
        "pdf": str(pdf_path),
        "pages": pages,
        "words": len(text.split()),
        "mentions": count,
        "outputs": {
            "extracted": str(extracted_path),
            "clean": str(clean_path),
            "mentions": str(mentions_path),
        },
    }


if __name__ == "__main__":
    import sys
    import json

    pdf_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("data")
    name = sys.argv[3] if len(sys.argv) > 3 else pdf_path.stem.lower().replace(" ", "_")

    result = process_pdf(pdf_path, output_dir, name)
    print(json.dumps(result, indent=2))
