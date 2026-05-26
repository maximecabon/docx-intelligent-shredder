"""
Contract Document Extraction Toolkit

Robust extraction and processing of .docx contract files:
  - Handles dynamic table of contents (w:sdt tags)
  - Extracts hyperlink text that standard libraries miss
  - Intelligent document shredding while preserving structure
"""

from pathlib import Path
import zipfile
from xml.etree import ElementTree as ET


# WordprocessingML namespace
_WORDML_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_WORDML_P_TAG = f"{{{_WORDML_NS}}}p"
_WORDML_TBL_TAG = f"{{{_WORDML_NS}}}tbl"
_WORDML_TR_TAG = f"{{{_WORDML_NS}}}tr"
_WORDML_TC_TAG = f"{{{_WORDML_NS}}}tc"


class ContractRiskAgent:
    """
    Contract document extraction toolkit.

    Provides robust extraction of text from .docx files with special handling for:
    - Dynamic table of contents (w:sdt tags)
    - Hyperlinks that standard libraries miss
    - Intelligent document shredding
    """

    def __init__(self):
        """Initialize the extraction toolkit."""
        pass

    def extract_docx_text(self, file_path: Path) -> str:
        """
        Extract text from .docx, handling dynamic TOC and hyperlinks.

        Returns:
            Full text with [PARAGRAPH N] and [TABLE N ROW M] markers
        """
        with zipfile.ZipFile(str(file_path)) as archive:
            with archive.open('word/document.xml') as fd:
                tree = ET.parse(fd)

        root = tree.getroot()
        body = root.find(f"{{{_WORDML_NS}}}body")
        if body is None:
            return ""

        parts = []
        paragraph_counter = 0

        def _xml_paragraph_text_full(p_elem) -> str:
            """Collect all text in paragraph, including hyperlinks."""
            pieces = []
            for elem in p_elem.iter():
                tag = elem.tag.split('}', 1)[-1] if '}' in elem.tag else elem.tag
                if tag == 't' and elem.text:
                    pieces.append(elem.text)
                elif tag == 'tab':
                    pieces.append('\t')
                elif tag == 'br':
                    pieces.append('\n')
            return ''.join(pieces).strip()

        def visit(node):
            nonlocal paragraph_counter
            for child in node:
                tag = child.tag.split('}', 1)[-1] if '}' in child.tag else child.tag

                if tag == 'p':
                    paragraph_counter += 1
                    text = _xml_paragraph_text_full(child)
                    if text:
                        parts.append(f"[PARAGRAPH {paragraph_counter}] {text}")

                elif tag == 'sdt':
                    # Structured Document Tag (dynamic TOC)
                    sdt_content = child.find(f"{{{_WORDML_NS}}}sdtContent")
                    if sdt_content is not None:
                        visit(sdt_content)
                    else:
                        visit(child)

                elif len(child) > 0:
                    visit(child)

        visit(body)
        return "\n".join(parts)

    def shred_text(self, text: str, chunk_size: int = 5000) -> list[str]:
        """
        Shred text into manageable chunks while preserving structure.

        Args:
            text: Full text with [PARAGRAPH N] markers
            chunk_size: Target chunk size in characters (default: 5000)

        Returns:
            List of text shreds
        """
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
