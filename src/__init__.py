"""DOCX text extraction and structured shredding toolkit."""

__version__ = "1.0.1"
__author__ = "Maxime Cabon"
__license__ = "MIT"

from .docx_shredder import DocxShredder, Shred, extract_docx_text, shred_text

__all__ = ["DocxShredder", "Shred", "extract_docx_text", "shred_text"]
