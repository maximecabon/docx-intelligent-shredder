# Changelog

## v1.0.0 (May 2026)

### 🎯 Initial Release: Document Extraction Toolkit

**What's Included:**
- ✅ Robust .docx text extraction with dynamic TOC and hyperlink support
- ✅ Intelligent document shredding while preserving structure
- ✅ Complete documentation and examples
- ✅ MIT open-source license

**Architecture:**
- `ContractRiskAgent` class with two core methods:
  - `extract_docx_text(file_path)` - Extract all text from .docx with proper handling of w:sdt and w:hyperlink elements
  - `shred_text(text, chunk_size)` - Break text into LLM-friendly chunks

**Documentation:**
- README.md - Quick start and usage examples
- docs/TOOL_SHRED_DOCX.md - Detailed technical implementation
- docs/BUG_HYPERLIENS_TOC_SYNTHESE.md - Root cause analysis and fix explanation
- docs/ROADMAP.md - Future phases (Clause extraction, Risk auditing, PDF support)

**Dependencies:**
- Python 3.9+
- Standard library only (zipfile, xml.etree)

### 🚧 Future Work (Not in v1.0)

These will be added in subsequent releases:
- Phase B: Clause extraction with LLM integration
- Phase C: Risk auditing framework  
- Excel report generation
- PDF support
- Multi-language support

### 📝 Why This Approach?

Rather than promise a complete multi-phase agent and deliver stubs, v1.0 focuses on what actually works: 
**robust document extraction**. This is the hard part that no standard library does well.

The extraction toolkit is reusable and can be integrated into any contract analysis pipeline. See README for examples.

---

**Author:** Maxime Cabon  
**License:** MIT  
**Repository:** https://github.com/[your-username]/contract-risk-agent
