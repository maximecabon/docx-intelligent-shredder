# Roadmap

## Current Scope

The repository contains one deterministic DOCX preprocessing tool:

- ordered extraction of document-body paragraphs;
- recovery of dynamic TOC and hyperlink text;
- extraction of table-row content;
- paragraph-aligned, lossless shredding with source-text offsets;
- standard-library unit tests with fictional fixture data.

It does not contain an audit agent, LLM integration or Excel reporting.

## Next Improvements

- Add fictional fixtures covering more Word XML variants.
- Support optional header and footer extraction.
- Expose structured paragraph/table records in addition to marked text.
- Validate behavior locally on non-published sample documents.
- Add packaging metadata for installation as a Python library.

## Separate Application Work

The following belong in an agent repository that depends on this tool, rather
than in this extraction library:

- human validation of a table of contents;
- tool-calling workflows for clause reconstruction;
- source anchoring checks for LLM-extracted clauses;
- definition interpretation and LoA analysis;
- spreadsheet reporting and review-state persistence.

## Known Limits

- Word `.docx` document body only.
- No PDF or OCR support.
- No semantic clause or index detection.
- No treatment of tracked-change meaning beyond visible XML text traversal.
