# docx-intelligent-shredder

**Smart document preprocessing for Word files.** Intelligently chunk large .docx files, extract sections by index, and prepare content for AI processing with full traceability.

## Overview

Large Word documents (100+ pages) break LLM context windows and lose structure. **docx-intelligent-shredder** solves this by:

1. **Reading the table of contents** intelligently (handles dynamic TOC, hyperlinks, nested sections)
2. **Chunking by logical sections** rather than arbitrary page breaks
3. **Extracting specific sections** on-demand based on the index
4. **Preparing clean content** for downstream AI/ML pipelines

### Three Use Cases

- **AI preparation**: Chunk large contracts/PDFs into context-aware segments for LLM analysis
- **Section extraction**: Pull specific chapters or sections by name directly from massive documents
- **Content preprocessing**: Extract and clean document structure before sending to pipelines

## Key Features

- ✅ **Robust .docx parsing**: Extracts dynamic tables of contents (handles `<w:sdt>` tags)
- ✅ **Hyperlink awareness**: Preserves text inside hyperlinks that standard tools miss
- ✅ **Intelligent chunking**: Uses document structure (headings, sections) not page breaks
- ✅ **Index-based extraction**: Get specific chapters or sections by name
- ✅ **Multiple output formats**: JSON, Markdown, text, or structured chunks
- ✅ **Zero dependencies on Word**: Pure Python XML parsing

## Installation

### Prerequisites

- Python 3.9+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/[your-username]/docx-intelligent-shredder.git
cd docx-intelligent-shredder

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Quick Start

```bash
# Shred a document into intelligent chunks
python src/docx_shredder.py shred path/to/document.docx

# Extract a specific section
python src/docx_shredder.py extract path/to/document.docx "Chapter 3: Definitions"

# Show table of contents
python src/docx_shredder.py toc path/to/document.docx
```

### Python API

```python
from docx_shredder import DocxShredder

# Initialize
shredder = DocxShredder("path/to/document.docx")

# Get table of contents
toc = shredder.get_toc()
print(toc)

# Chunk the entire document
chunks = shredder.chunk_by_sections()
for chunk in chunks:
    print(f"Section: {chunk['title']}")
    print(f"Content: {chunk['text'][:100]}...")

# Extract a specific section
section = shredder.extract_section("Chapter 2: Scope")
print(section['text'])

# Get metadata
print(shredder.get_metadata())
```

### Output Formats

The tool produces:

- **JSON chunks**: Machine-readable sections with metadata
- **Markdown**: Readable format with hierarchy preserved
- **Plain text**: Clean text for LLM processing
- **Metadata**: Document structure, section count, word count

## Examples

### Example 1: Prepare contract for LLM analysis

```python
shredder = DocxShredder("contract.docx")
chunks = shredder.chunk_by_sections(max_tokens=2000)

for chunk in chunks:
    # Send to LLM for analysis
    response = llm.analyze(chunk['text'])
    print(f"{chunk['title']}: {response}")
```

### Example 2: Extract definitions section

```python
shredder = DocxShredder("legal_doc.docx")
definitions = shredder.extract_section("Definitions")
print(definitions['text'])
```

### Example 3: Batch process multiple documents

```python
import os
from docx_shredder import DocxShredder

for filename in os.listdir("contracts/"):
    if filename.endswith(".docx"):
        shredder = DocxShredder(f"contracts/{filename}")
        chunks = shredder.chunk_by_sections()
        # Process chunks...
```

## Architecture

### How It Works

1. **Parse .docx XML**: Extract raw content and structure from the Word XML
2. **Build TOC**: Identify all headings and sections (handles dynamic TOC)
3. **Create logical chunks**: Group content by section boundaries, not pages
4. **Index sections**: Map section names to content for quick lookup
5. **Output**: Serialize to JSON, Markdown, or text format

### Technical Details

- **Dynamic TOC handling**: Parses `<w:sdt>` (Structured Document Tags) for real tables of contents
- **Hyperlink preservation**: Captures text inside `<w:hyperlink>` that standard tools lose
- **Section awareness**: Uses heading levels to maintain document hierarchy
- **Token counting**: Optional token estimation for LLM context windows

See `docs/TOOL_SHRED_DOCX.md` for implementation details.

## Documentation

- **[TOOL_SHRED_DOCX.md](docs/TOOL_SHRED_DOCX.md)**: Deep dive into .docx extraction and XML parsing
- **[ROADMAP.md](docs/ROADMAP.md)**: Planned features and improvements
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: How to contribute

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Quick summary:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Write tests for new functionality
4. Commit with clear messages
5. Push and open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) for details.

## Questions?

- Open an issue on GitHub
- Check [docs](docs/) for detailed documentation
- Email: maxime.cabon@gmail.com

---

**Author:** Maxime Cabon  
**Email:** maxime.cabon@gmail.com  
**Version:** 1.0.0  
**Last Updated:** May 2026
