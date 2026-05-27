# Project Notes

This file captures ideas that emerge during development but should NOT be added to v0.1.
v0.1 scope is locked. Ideas here become inputs for future versions.

## 2026-05-24

## 2026-05-26

- Pivoted from full transcript to Published Script (prepared remarks)
- Q&A not available in legal/free public sources
- See cs_projs_notes/lesson_learned.md for broader takeaways-

## 2026-05-26 Day 4: PDF Extraction Quality Check

### Verified clean

- No tables in source PDF
- Numbers + units preserved correctly ($7.91 billion etc)
- Special chars (|, &) render correctly  
- No bullet points in source

### Found issue (non-blocking)

- Paragraph structure not fully preserved: each sentence in
  source PDF ends up on its own line after extraction
- Original paragraphs (multiple sentences) become
  multi-line blocks
- Impact: may affect LLM's ability to recognize
  connected narrative across sentences
- Resolution: paragraph reconstruction step needed in
  Day 5 preprocessing pipeline

### Word count finding

- 2,814 words for AMAT prepared remarks
- Lower than typical (4,000-7,000)
- AMAT IR style is concise
