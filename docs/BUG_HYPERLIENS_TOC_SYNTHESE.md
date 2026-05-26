# Dynamic TOC and Hyperlink Extraction Note

## Problem

A Word document may visibly contain a table of contents while a high-level
DOCX library returns none of its entry text. This happens when Word stores the
TOC as a field inside a Structured Document Tag (`w:sdt`) and stores visible
entries inside hyperlink elements (`w:hyperlink`).

## Root Cause

An extractor that reads only ordinary top-level paragraphs can miss:

- paragraphs nested under `w:sdtContent`;
- visible runs nested under hyperlinks;
- text contained in table cells.

The issue is an extraction-layer issue, not evidence that a document lacks an
index.

## Implemented Approach

`src/docx_shredder.py` reads `word/document.xml` directly and traverses the
body in document order. It handles:

- `w:sdt` / `w:sdtContent` for dynamic TOC content;
- all descendant `w:t` elements in a paragraph, which includes hyperlinks;
- `w:tab` and `w:br` markers;
- table rows and cells.

The resulting markers are stable for downstream processing:

```text
[PARAGRAPH N] text
[TABLE N ROW M] cell text | next cell text
```

## Regression Protection

`tests/test_docx_shredder.py` generates a fictional minimal DOCX archive in a
temporary directory and checks dynamic TOC text, hyperlink text and table-row
extraction. No document supplied by a user is committed to the repository.

## Files

- `src/docx_shredder.py`: deterministic production tool.
- `tests/test_docx_shredder.py`: fictional regression fixture.
- `docs/TOOL_SHRED_DOCX.md`: API and integration details.
