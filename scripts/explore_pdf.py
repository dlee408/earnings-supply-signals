import pdfplumber
from pathlib import Path

PDF_PATH = Path("data") / "Q2 2026 Earnings Call Published Script.pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    print(f"---")

    # Extract text from each page
    full_text = ""
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        full_text += text + "\n"
        print(f"Page {i +1}: {len(text)} characters")

    print(f"---")
    print(f"Total characters: {len(full_text)}")
    print(f"Estimated words: {len(full_text.split())}")
    print(f"---")
    print("First 500 charts:")
    print(f"---")
    print(full_text[:500])
    print(f"---")
    print("Last 500 charts:")
    print(f"---")
    print(full_text[-500:])

# Save extracted text for review
output_path = Path("data") / "amat_q2_2026_extracted.txt"
output_path.write_text(full_text)
print(f"Saved extracted text to {output_path}")
