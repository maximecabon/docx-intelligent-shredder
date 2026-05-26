"""
Contract Risk Agent - Document Extraction Toolkit

Robust extraction of .docx contract files with special handling for:
- Dynamic tables of contents (w:sdt tags)
- Hyperlinks (w:hyperlink elements)
- Intelligent document shredding for LLM processing
"""

__version__ = "1.0.0"
__author__ = "Maxime Cabon"
__license__ = "MIT"

from .contract_risk_agent import ContractRiskAgent

__all__ = ["ContractRiskAgent"]
