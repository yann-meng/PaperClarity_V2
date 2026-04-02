import json

from sqlmodel import Session, select

from db.tables import BlockTable, DocumentTable, EquationTable, SectionTable
from models.block import Block
from models.document import Document
from models.equation import Equation
from models.section import Section


class DocumentRepository:
    def upsert_document(self, session: Session, document: Document) -> None:
        row = session.get(DocumentTable, document.id)
        metadata_json = json.dumps(document.metadata, ensure_ascii=False)
        if row is None:
            row = DocumentTable(
                id=document.id,
                title=document.title,
                source_path=document.source_path,
                doc_type=document.doc_type,
                metadata_json=metadata_json,
            )
            session.add(row)
        else:
            row.title = document.title
            row.source_path = document.source_path
            row.metadata_json = metadata_json

        session.exec(select(BlockTable).where(BlockTable.document_id == document.id)).all()
        for table in [BlockTable, SectionTable, EquationTable]:
            old_rows = session.exec(select(table).where(table.document_id == document.id)).all()
            for item in old_rows:
                session.delete(item)

        for block in document.blocks:
            session.add(
                BlockTable(
                    id=block.id,
                    document_id=document.id,
                    page=block.page,
                    section_id=block.section_id,
                    block_type=block.block_type,
                    text=block.text,
                    bbox_json=json.dumps(block.bbox or []),
                    order=block.order,
                )
            )
        for section in document.sections:
            session.add(
                SectionTable(
                    id=section.id,
                    document_id=document.id,
                    title=section.title,
                    level=section.level,
                    start_block_id=section.start_block_id,
                    end_block_id=section.end_block_id,
                )
            )
        for equation in document.equations:
            session.add(
                EquationTable(
                    id=equation.id,
                    document_id=document.id,
                    page=equation.page,
                    raw_text=equation.raw_text,
                    latex=equation.latex,
                    block_id=equation.block_id,
                    symbols_json=json.dumps(equation.symbols, ensure_ascii=False),
                )
            )
        session.commit()

    def get_document(self, session: Session, document_id: str) -> Document | None:
        doc_row = session.get(DocumentTable, document_id)
        if doc_row is None:
            return None
        blocks = [
            Block(
                id=b.id,
                page=b.page,
                section_id=b.section_id,
                block_type=b.block_type,
                text=b.text,
                bbox=json.loads(b.bbox_json),
                order=b.order,
            )
            for b in session.exec(
                select(BlockTable)
                .where(BlockTable.document_id == document_id)
                .order_by(BlockTable.page, BlockTable.order)
            ).all()
        ]
        sections = [
            Section(
                id=s.id,
                title=s.title,
                level=s.level,
                start_block_id=s.start_block_id,
                end_block_id=s.end_block_id,
            )
            for s in session.exec(select(SectionTable).where(SectionTable.document_id == document_id)).all()
        ]
        equations = [
            Equation(
                id=e.id,
                page=e.page,
                raw_text=e.raw_text,
                latex=e.latex,
                block_id=e.block_id,
                symbols=json.loads(e.symbols_json),
            )
            for e in session.exec(select(EquationTable).where(EquationTable.document_id == document_id)).all()
        ]
        return Document(
            id=doc_row.id,
            title=doc_row.title,
            source_path=doc_row.source_path,
            doc_type=doc_row.doc_type,
            metadata=json.loads(doc_row.metadata_json),
            blocks=blocks,
            sections=sections,
            equations=equations,
        )
