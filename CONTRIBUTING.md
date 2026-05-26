# Contributing to docx-intelligent-shredder

Thank you for your interest in contributing! This project welcomes all improvements, bug fixes, and feature proposals.

## How to Contribute

### Reporting Bugs

1. Check existing [issues](https://github.com/[your-username]/docx-intelligent-shredder/issues) first
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs. actual behavior
   - Document type and size (if relevant)
   - Python version and OS

### Suggesting Features

1. Open an issue labeled `enhancement`
2. Describe the use case and expected behavior
3. Explain how it would improve document preprocessing

### Submitting Code

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/your-feature`
3. **Write tests** for new functionality
4. **Follow the code style** (PEP 8, type hints preferred)
5. **Commit with clear messages**: `git commit -m "Add feature: description"`
6. **Push** and open a **Pull Request**

### Code Style

- Follow PEP 8
- Use type hints for function parameters and returns
- Write docstrings for public functions
- Keep functions focused and testable

Example:
```python
def extract_toc(docx_path: str) -> list[dict]:
    """
    Extract table of contents from a Word document.
    
    Args:
        docx_path: Path to the .docx file
    
    Returns:
        List of TOC entries with hierarchy levels
    """
```

### Testing

Before submitting, ensure:
- New code has unit tests
- All tests pass: `pytest`
- No regression in existing tests

### Documentation

Update relevant documentation:
- README.md (if changing usage)
- ROADMAP.md (if adding features)
- Code comments (for complex logic)
- CONTRIBUTING.md (if changing contribution process)

## Project Structure

```
docx-intelligent-shredder/
├── src/
│   ├── docx_shredder.py (main module)
│   └── utils/
├── docs/
│   ├── TOOL_SHRED_DOCX.md
│   └── ROADMAP.md
├── tests/
├── README.md
├── LICENSE
└── requirements.txt
```

## Questions?

- Check existing discussions
- Open an issue for clarification
- Email: maxime.cabon@gmail.com

## Recognition

All contributors are listed in CONTRIBUTORS.md. Thank you for making this project better!
