import fitz

from services.pdf_parser import PdfParser


def test_pdf_parser_extracts_blocks(tmp_path) -> None:
    pdf_path = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "1 Introduction\n\nThis is a test paragraph with x = y + z")
    doc.save(pdf_path)
    doc.close()

    parser = PdfParser()
    parsed = parser.parse(str(pdf_path))
    assert len(parsed.blocks) >= 1
    assert parsed.metadata["page_count"] == 1
