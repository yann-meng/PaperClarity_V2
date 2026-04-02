import re
from pathlib import Path

import fitz

from models.block import Block
from models.document import Document
from models.equation import Equation
from services.chunker import chunk_text
from services.structure_extractor import extract_sections

EQUATION_PATTERN = re.compile(r"(=|\\sum|\\min|\\max|\\log|\\mathbb|\\lambda)")


class PdfParser:
    def parse(self, file_path: str) -> Document:
        pdf = fitz.open(file_path)
        doc_id = Path(file_path).stem.replace(" ", "_")
        blocks: list[Block] = []
        equations: list[Equation] = []
        order = 0
        for page_index, page in enumerate(pdf, start=1):
            text = page.get_text("text")
            for chunk in chunk_text(text):
                block_id = f"b_{page_index}_{order}"
                block = Block(id=block_id, page=page_index, text=chunk, order=order)
                blocks.append(block)
                if EQUATION_PATTERN.search(chunk):
                    equations.append(
                        Equation(
                            id=f"eq_{page_index}_{order}",
                            page=page_index,
                            raw_text=chunk,
                            block_id=block_id,
                        )
                    )
                order += 1
        sections = extract_sections(blocks)
        return Document(
            id=doc_id,
            title=Path(file_path).stem,
            source_path=file_path,
            doc_type="pdf",
            metadata={"page_count": len(pdf)},
            sections=sections,
            blocks=blocks,
            equations=equations,
        )
