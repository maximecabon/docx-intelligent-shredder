# docx-intelligent-shredder

Small, dependency-free Python toolkit for extracting ordered text from Word
`.docx` documents and splitting that text into bounded fragments for downstream
processing.

## What It Does

- Reads `word/document.xml` directly from a `.docx` archive.
- Includes text inside dynamic Word table-of-contents containers (`w:sdt`).
- Includes text inside hyperlinks (`w:hyperlink`), including linked TOC entries.
- Extracts table rows as structured text markers.
- Splits extracted text into size-bounded shreds while preserving complete
  extracted lines whenever possible.
- Returns character offsets for each shred so downstream systems can retain
  traceability to the extracted source text.

## What It Does Not Do

- It does not identify clauses semantically.
- It does not validate or interpret a table of contents.
- It does not call an LLM or an API.
- It does not audit risks or produce Excel reports.
- It does not currently read headers, footers, comments, OCR, or PDFs.

Those responsibilities belong in applications built on top of this tool.

## Requirements

- Python 3.9 or later
- No third-party packages

## Usage

Extract document text:

```powershell
python src\docx_shredder.py extract path\to\contract.docx
```

Extract and split into JSON shreds:

```powershell
python src\docx_shredder.py shred path\to\contract.docx --max-chars 12000
```

Python API:

```python
from src.docx_shredder import DocxShredder

shredder = DocxShredder("contract.docx")
text = shredder.extract_text()
shreds = shredder.shred(max_chars=12000)

for shred in shreds:
    print(shred.shred_id, shred.start_char, shred.end_char)
    print(shred.text)
```

The functional API is also available:

```python
from src.docx_shredder import extract_docx_text, shred_text

text = extract_docx_text("contract.docx")
shreds = shred_text(text, max_chars=12000)
```

## Output Markers

The text extractor returns lines such as:

```text
[PARAGRAPH 1] SAMPLE AGREEMENT
[PARAGRAPH 2] 1. Definitions    5
[TABLE 1 ROW 1] Term | Meaning
[PARAGRAPH 3] Clause 1. Definitions
```

These markers preserve ordering and provide a stable representation for
applications that perform clause extraction or index validation later.

## Testing

Run the standard-library test suite:

```powershell
python -m unittest discover -s tests -v
```

The tests cover dynamic TOC extraction, hyperlink text, table rows, wrapper
usage and lossless shredding. They generate only a fictional minimal DOCX
fixture; no real contract content is stored in this repository.

## Repository Layout

```text
src/docx_shredder.py        Extraction and shredding implementation
tests/test_docx_shredder.py Unit tests with fictional fixture data
docs/TOOL_SHRED_DOCX.md     Technical behavior and integration notes
docs/BUG_HYPERLIENS_TOC_SYNTHESE.md Root-cause notes for TOC/hyperlink loss
docs/ROADMAP.md             Planned extensions
```

## License

MIT License. See [LICENSE](LICENSE).
