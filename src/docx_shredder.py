"""Reliable DOCX text extraction and paragraph-aligned shredding.

This module is deliberately limited to document preprocessing. It extracts
text from the WordprocessingML document body, including content inside dynamic
table-of-contents containers and hyperlinks, then produces bounded text
shreds for downstream systems.
"""

from __future__ import annotations

import argparse
import json
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


_WORDML_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_WORDML_TR_TAG = f"{{{_WORDML_NS}}}tr"
_WORDML_TC_TAG = f"{{{_WORDML_NS}}}tc"


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _paragraph_text(p_elem: ET.Element) -> str:
    """Return paragraph text, including descendants such as hyperlinks."""

    pieces: list[str] = []
    for elem in p_elem.iter():
        tag = _local_name(elem.tag)
        if tag == "t" and elem.text:
            pieces.append(elem.text)
        elif tag == "tab":
            pieces.append("\t")
        elif tag == "br":
            pieces.append("\n")
    return "".join(pieces).strip()


def extract_docx_text(file_path: str | Path) -> str:
    """Extract ordered body text from a DOCX file.

    Output uses stable markers:
    - ``[PARAGRAPH N]`` for non-table paragraphs;
    - ``[TABLE N ROW M]`` for non-empty table rows.

    Dynamic TOC text wrapped in ``w:sdt`` and text held by hyperlinks are
    included because traversal is performed directly on WordprocessingML.
    """

    path = Path(file_path)
    if path.suffix.lower() != ".docx":
        raise ValueError(f"Expected a .docx file: {path}")
    if not path.exists():
        raise FileNotFoundError(path)

    try:
        with zipfile.ZipFile(path) as archive:
            with archive.open("word/document.xml") as document_xml:
                tree = ET.parse(document_xml)
    except (zipfile.BadZipFile, KeyError, ET.ParseError) as exc:
        raise ValueError(f"Invalid DOCX document: {path}") from exc

    body = tree.getroot().find(f"{{{_WORDML_NS}}}body")
    if body is None:
        return ""

    parts: list[str] = []
    paragraph_counter = 0
    table_counter = 0

    def visit(node: ET.Element, cell_pieces: list[str] | None = None) -> None:
        nonlocal paragraph_counter, table_counter
        for child in node:
            tag = _local_name(child.tag)
            if tag == "p":
                text = _paragraph_text(child)
                if cell_pieces is not None:
                    if text:
                        cell_pieces.append(text)
                    continue
                paragraph_counter += 1
                if text:
                    parts.append(f"[PARAGRAPH {paragraph_counter}] {text}")
                continue

            if tag == "tbl" and cell_pieces is None:
                table_counter += 1
                for row_idx, row in enumerate(child.findall(_WORDML_TR_TAG), start=1):
                    cells: list[str] = []
                    for cell in row.findall(_WORDML_TC_TAG):
                        current_cell: list[str] = []
                        visit(cell, cell_pieces=current_cell)
                        text = " ".join(current_cell).strip()
                        if text:
                            cells.append(text)
                    if cells:
                        parts.append(
                            f"[TABLE {table_counter} ROW {row_idx}] "
                            + " | ".join(cells)
                        )
                continue

            if tag == "sdt":
                content = child.find(f"{{{_WORDML_NS}}}sdtContent")
                visit(content if content is not None else child, cell_pieces=cell_pieces)
                continue

            if len(child):
                visit(child, cell_pieces=cell_pieces)

    visit(body)
    return "\n".join(parts)


@dataclass(frozen=True)
class Shred:
    """A source-aligned text fragment."""

    shred_id: int
    start_char: int
    end_char: int
    text: str

    def as_dict(self) -> dict[str, int | str]:
        return asdict(self)


def shred_text(text: str, max_chars: int = 12000) -> list[Shred]:
    """Split extracted text into bounded shreds while preserving full lines.

    Lines are retained intact whenever their own length is no greater than
    ``max_chars``. An exceptionally long individual line is split only when
    unavoidable. Concatenating all returned ``text`` values recreates the
    input exactly.
    """

    if max_chars <= 0:
        raise ValueError("max_chars must be greater than zero")
    if not text:
        return []

    shreds: list[Shred] = []
    current_parts: list[str] = []
    current_start = 0
    position = 0

    def flush() -> None:
        nonlocal current_parts, current_start
        if not current_parts:
            return
        content = "".join(current_parts)
        shreds.append(
            Shred(
                shred_id=len(shreds) + 1,
                start_char=current_start,
                end_char=current_start + len(content),
                text=content,
            )
        )
        current_parts = []

    for line in text.splitlines(keepends=True):
        if len(line) > max_chars:
            flush()
            for offset in range(0, len(line), max_chars):
                part = line[offset : offset + max_chars]
                shreds.append(
                    Shred(
                        shred_id=len(shreds) + 1,
                        start_char=position + offset,
                        end_char=position + offset + len(part),
                        text=part,
                    )
                )
            position += len(line)
            current_start = position
            continue

        if current_parts and sum(len(part) for part in current_parts) + len(line) > max_chars:
            flush()
            current_start = position
        elif not current_parts:
            current_start = position
        current_parts.append(line)
        position += len(line)

    flush()
    return shreds


class DocxShredder:
    """Small reusable wrapper around extraction and shredding functions."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def extract_text(self) -> str:
        return extract_docx_text(self.file_path)

    def shred(self, max_chars: int = 12000) -> list[Shred]:
        return shred_text(self.extract_text(), max_chars=max_chars)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract or shred text from a DOCX file.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser("extract", help="Print extracted document text.")
    extract_parser.add_argument("document", type=Path)

    shred_parser = subparsers.add_parser("shred", help="Print shreds as JSON.")
    shred_parser.add_argument("document", type=Path)
    shred_parser.add_argument("--max-chars", type=int, default=12000)

    args = parser.parse_args(argv)
    shredder = DocxShredder(args.document)
    if args.command == "extract":
        print(shredder.extract_text())
        return 0

    print(
        json.dumps(
            [item.as_dict() for item in shredder.shred(args.max_chars)],
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
