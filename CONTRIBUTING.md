# Contributing

This repository is intentionally scoped to deterministic DOCX extraction and
shredding. Changes should preserve that focus.

## Development

The tool uses Python standard-library modules only. Run tests before submitting
a change:

```powershell
python -m unittest discover -s tests -v
```

## Good Contributions

- Additional fictional DOCX XML fixtures and regression tests.
- Fixes for loss of visible text or incorrect ordering.
- Clearer source-offset or shred-boundary behavior.
- Documentation corrections that match implemented behavior.

Do not commit real contracts, extracted contract text, execution traces,
credentials or generated review outputs.

Features involving LLMs, clause assessment, Excel reports or legal workflow
orchestration should be implemented in a separate application repository.

## Layout

```text
src/docx_shredder.py
tests/test_docx_shredder.py
docs/
README.md
```
