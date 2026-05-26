#!/usr/bin/env python3
"""
Contract Risk Audit Agent

Main entry point for contract risk auditing workflow.
Orchestrates three phases:
  1. Table of Contents extraction (Phase A)
  2. Clause extraction (Phase B)
  3. Risk exposure auditing

Usage:
  python contract_risk_audit_agent.py run
  python contract_risk_audit_agent.py resume --state-dir "path/to/run"
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from contract_risk_agent import ContractRiskAgent


class ContractRiskAuditAgent:
    """
    Audit contractual risks across extracted clauses.

    Workflow:
    1. Extract and validate table of contents
    2. Extract clauses with contextual memory
    3. For each contractual risk exposure, verify compliance
    4. Generate Excel report with traceability
    """

    def __init__(
        self,
        llm_provider: str = "ollama",
        model: str = "llama2",
        contract_path: Optional[Path] = None,
        review_name: Optional[str] = None,
        validate_index: bool = True,
        validate_clauses: bool = True,
        clause_granularity: str = "clause",
        max_definitions_chars: int = 100000,
    ):
        """
        Initialize the audit agent.

        Args:
            llm_provider: LLM to use ("ollama", "openai", "openai-compatible")
            model: Model name
            contract_path: Path to .docx contract
            review_name: Name for output directory
            validate_index: Whether to validate TOC interactively
            validate_clauses: Whether to validate extracted clauses
            clause_granularity: "clause" or "subclause"
            max_definitions_chars: Max context for contractual definitions
        """
        self.agent = ContractRiskAgent(
            llm_provider=llm_provider,
            model=model,
        )
        self.contract_path = contract_path
        self.review_name = review_name
        self.validate_index = validate_index
        self.validate_clauses = validate_clauses
        self.clause_granularity = clause_granularity
        self.max_definitions_chars = max_definitions_chars

    def run(self) -> None:
        """Execute full audit workflow."""
        print("Starting Contract Risk Audit Agent...")
        print(f"Contract: {self.contract_path}")
        print(f"Review: {self.review_name}")
        print()

        # Phase A: Table of Contents extraction
        print("=" * 60)
        print("PHASE A: Table of Contents Extraction")
        print("=" * 60)
        toc_entries = self.agent.extract_toc(
            self.contract_path,
            validate=self.validate_index,
        )
        print(f"✓ Extracted {len(toc_entries)} TOC entries")
        print()

        # Phase B: Clause extraction
        print("=" * 60)
        print("PHASE B: Clause Extraction")
        print("=" * 60)
        clauses = self.agent.extract_clauses(
            self.contract_path,
            toc_entries=toc_entries,
            validate=self.validate_clauses,
            granularity=self.clause_granularity,
        )
        print(f"✓ Extracted {len(clauses)} clauses")
        print()

        # Phase C: Risk audit
        print("=" * 60)
        print("PHASE C: Risk Exposure Audit")
        print("=" * 60)
        risk_framework = self._load_risk_framework()
        audit_results = self.agent.audit_risks(
            clauses=clauses,
            risk_framework=risk_framework,
            definitions_limit=self.max_definitions_chars,
        )
        print(f"✓ Audited {len(risk_framework)} risk exposures")
        print()

        # Generate outputs
        print("=" * 60)
        print("Generating Reports")
        print("=" * 60)
        self.agent.generate_excel_report(
            audit_results,
            output_dir=self.review_name,
        )
        print(f"✓ Excel report: {self.review_name}/MR_identification.xlsx")
        print(f"✓ JSON files in: {self.review_name}/")
        print()
        print("Audit complete.")

    def resume(self, state_dir: Path) -> None:
        """Resume an interrupted audit from saved state."""
        print(f"Resuming from: {state_dir}")
        # Implementation would load state and continue
        pass

    def _load_risk_framework(self) -> dict:
        """Load or prompt for contractual risk framework."""
        # Implementation would load from file or prompt user
        return {}


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Contract Risk Audit Agent"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Run command
    run_parser = subparsers.add_parser("run", help="Start a new audit")
    run_parser.add_argument(
        "--llm-provider",
        default="ollama",
        choices=["ollama", "openai", "openai-compatible"],
        help="LLM provider",
    )
    run_parser.add_argument(
        "--model",
        help="Model name",
    )
    run_parser.add_argument(
        "--contract",
        type=Path,
        help="Path to .docx contract",
    )
    run_parser.add_argument(
        "--review-name",
        help="Name for review output directory",
    )
    run_parser.add_argument(
        "--no-validate-index",
        action="store_true",
        help="Skip TOC validation",
    )
    run_parser.add_argument(
        "--no-validate-clauses",
        action="store_true",
        help="Skip clause validation",
    )
    run_parser.add_argument(
        "--clause-granularity",
        choices=["clause", "subclause"],
        default="clause",
        help="Clause granularity level",
    )
    run_parser.add_argument(
        "--max-definitions-chars",
        type=int,
        default=100000,
        help="Max chars for definitions context",
    )

    # Resume command
    resume_parser = subparsers.add_parser("resume", help="Resume interrupted audit")
    resume_parser.add_argument(
        "--state-dir",
        type=Path,
        required=True,
        help="Directory with saved state",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "run":
        agent = ContractRiskAuditAgent(
            llm_provider=args.llm_provider,
            model=args.model or "default",
            contract_path=args.contract,
            review_name=args.review_name or "default_review",
            validate_index=not args.no_validate_index,
            validate_clauses=not args.no_validate_clauses,
            clause_granularity=args.clause_granularity,
            max_definitions_chars=args.max_definitions_chars,
        )
        agent.run()

    elif args.command == "resume":
        agent = ContractRiskAuditAgent()
        agent.resume(args.state_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
