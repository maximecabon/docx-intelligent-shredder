# DOCX Extraction Tool

## Purpose

`src/docx_shredder.py` is a standalone preprocessing tool. It extracts the
visible text held in a Word document body and supplies bounded text shreds for
downstream applications such as a contract-analysis agent.

The tool deliberately does not classify clauses, call an LLM or make legal
decisions.

## Public API

```python
def extract_docx_text(file_path: str | Path) -> str
def shred_text(text: str, max_chars: int = 12000) -> list[Shred]

class DocxShredder:
    def extract_text(self) -> str
    def shred(self, max_chars: int = 12000) -> list[Shred]
```

Each `Shred` contains:

```python
shred_id: int
start_char: int
end_char: int
text: str
```

The `start_char` and `end_char` offsets address the extracted text returned by
`extract_docx_text`, not the binary Word file.

## XML Handling

A `.docx` is a ZIP archive. The extractor reads `word/document.xml` and walks
the `w:body` tree in document order.

Supported structures:

- ordinary paragraphs (`w:p`);
- text runs (`w:t`);
- tabs and line breaks (`w:tab`, `w:br`);
- hyperlink-contained runs (`w:hyperlink`) by descending through paragraph
  descendants;
- dynamic table of contents content (`w:sdt` / `w:sdtContent`);
- non-empty table rows (`w:tbl`, `w:tr`, `w:tc`).

Output markers:

```text
[PARAGRAPH N] text
[TABLE N ROW M] cell text | next cell text
```

## Shredding Behavior

`shred_text` works on extracted text. It groups complete extracted lines until
adding another line would exceed `max_chars`. If one individual line is
larger than the limit, that line is split because no line-preserving result is
possible.

Safety invariant:

```python
"".join(shred.text for shred in shred_text(text)) == text
```

This invariant allows a downstream agent to check that it has not lost content
during preprocessing.

## Intended Integration With An Agent

The tool should be used as a deterministic first stage:

1. Extract source text with `extract_docx_text`.
2. Create shreds with `shred_text`.
3. Pass those shreds to a separate index- or clause-extraction workflow.
4. Retain offsets and original extracted text for verification.

An agent that later accepts clause text from a model should verify that the
text is anchored in the extracted source. That safeguard is outside this tool
because this package does not make model calls.

## Confidentiality

This repository contains code and fictional unit-test fixture text only. Real
contract documents and extracted output must remain outside version control.

## Known Limits

- Only the document body is extracted; headers and footers are excluded.
- Deleted text and revision semantics are not interpreted separately.
- Images, SmartArt, equations and OCR text are not extracted.
- PDF input is not supported.
- Semantic TOC or clause parsing is intentionally outside scope.
