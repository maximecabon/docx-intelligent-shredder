# Roadmap

## Current Status: Document Extraction Toolkit (v1.0)

**What's implemented:**
- ✅ Robust .docx text extraction (with dynamic TOC + hyperlink support)
- ✅ Intelligent document shredding
- ✅ Reusable toolkit for building contract analysis pipelines

**What's NOT in v1.0 (future phases):**
- 🚧 LLM integration for clause extraction (Phase B)
- 🚧 Risk auditing framework (Phase C)
- 🚧 Excel report generation

## Short Term (1 Month)

### Phase B: Clause Extraction Framework
- Define and implement stateful clause extraction
- Add example implementations for different LLMs (Claude, GPT-4, Llama)
- Include memory management across shreds

### Phase C: Risk Auditing Framework
- Define contractual risk exposure model
- Build audit logic across extracted clauses
- Generate structured output (JSON/Excel)

## Medium Term (6 Months)

### PDF Support
- Direct parsing of PDF-format contracts
- Don't rely on Word as intermediate format
- Option for OCR on scanned PDFs

### Multi-Language Support
- Handle contracts in French, Spanish, German, etc.
- Preserve language detection metadata

### Template Comparison
- Load reference contract templates
- Auto-detect deviations from standard clauses
- Generate redlines automatically

## Future Considerations

- Integration with legal databases (LexisNexis, Bloomberg Law)
- Automated redline generation in track-changes format (.docx)
- Bulk contract processing pipeline
- API interface for third-party integration
- Web UI for non-technical users
- Jurisdiction-specific legal benchmarking
- Comment and tracked-changes extraction

## Known Limitations

Current version:
- English-language contracts only (extensible)
- Tested on EPC and industrial contracts; other types untested
- Hyperlinks must be properly formed (can't infer missing links)
- Very large contracts (500+ pages) may need splitting manually
- Word documents only (PDF support planned)

## Contributing

Have an idea? Open an issue or pull request. Priority goes to improvements that:
1. Extend extraction robustness (edge cases in .docx parsing)
2. Add reusable building blocks for contract analysis
3. Maintain code quality and testability
4. Don't require expensive external dependencies
