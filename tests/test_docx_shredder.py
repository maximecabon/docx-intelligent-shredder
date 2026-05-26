from __future__ import annotations

import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from docx_shredder import DocxShredder, extract_docx_text, shred_text  # noqa: E402


DOCUMENT_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>SAMPLE AGREEMENT</w:t></w:r></w:p>
    <w:sdt><w:sdtContent>
      <w:p>
        <w:hyperlink><w:r><w:t>1. Definitions</w:t></w:r></w:hyperlink>
        <w:r><w:tab/><w:t>5</w:t></w:r>
      </w:p>
    </w:sdtContent></w:sdt>
    <w:tbl>
      <w:tr>
        <w:tc><w:p><w:r><w:t>Term</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:t>Meaning</w:t></w:r></w:p></w:tc>
      </w:tr>
    </w:tbl>
    <w:p><w:r><w:t>Clause 1. Definitions</w:t></w:r></w:p>
  </w:body>
</w:document>
"""


def build_docx(directory: Path) -> Path:
    path = directory / "sample.docx"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", DOCUMENT_XML)
    return path


class ExtractDocxTextTests(unittest.TestCase):
    def test_extracts_dynamic_toc_hyperlink_and_table(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = extract_docx_text(build_docx(Path(tmp)))

        self.assertIn("[PARAGRAPH 1] SAMPLE AGREEMENT", output)
        self.assertIn("[PARAGRAPH 2] 1. Definitions\t5", output)
        self.assertIn("[TABLE 1 ROW 1] Term | Meaning", output)
        self.assertIn("[PARAGRAPH 3] Clause 1. Definitions", output)

    def test_wrapper_extracts_document(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            shredder = DocxShredder(build_docx(Path(tmp)))
            self.assertIn("SAMPLE AGREEMENT", shredder.extract_text())

    def test_rejects_non_docx_paths(self) -> None:
        with self.assertRaises(ValueError):
            extract_docx_text("contract.pdf")


class ShredTextTests(unittest.TestCase):
    def test_shreds_preserve_text_and_line_boundaries(self) -> None:
        text = "[PARAGRAPH 1] ABC\n[PARAGRAPH 2] DEF\n[PARAGRAPH 3] GHI"
        shreds = shred_text(text, max_chars=38)

        self.assertGreater(len(shreds), 1)
        self.assertEqual("".join(item.text for item in shreds), text)
        self.assertEqual(shreds[0].start_char, 0)
        self.assertEqual(shreds[-1].end_char, len(text))

    def test_oversized_line_is_split_without_losing_content(self) -> None:
        text = "A" * 25
        shreds = shred_text(text, max_chars=10)
        self.assertEqual([len(item.text) for item in shreds], [10, 10, 5])
        self.assertEqual("".join(item.text for item in shreds), text)

    def test_rejects_invalid_limit(self) -> None:
        with self.assertRaises(ValueError):
            shred_text("text", max_chars=0)


if __name__ == "__main__":
    unittest.main()
