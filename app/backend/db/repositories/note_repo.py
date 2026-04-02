import json

from sqlmodel import Session, select

from db.tables import NoteTable
from models.note import Note, NoteCreate


class NoteRepository:
    def create(self, session: Session, payload: NoteCreate) -> Note:
        row = NoteTable(
            document_id=payload.document_id,
            title=payload.title,
            content=payload.content,
            citations_json=json.dumps(payload.citations, ensure_ascii=False),
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return Note(
            id=row.id or 0,
            document_id=row.document_id,
            title=row.title,
            content=row.content,
            citations=json.loads(row.citations_json),
            created_at=row.created_at,
        )

    def list_by_document(self, session: Session, document_id: str) -> list[Note]:
        rows = session.exec(
            select(NoteTable).where(NoteTable.document_id == document_id).order_by(NoteTable.created_at.desc())
        ).all()
        return [
            Note(
                id=row.id or 0,
                document_id=row.document_id,
                title=row.title,
                content=row.content,
                citations=json.loads(row.citations_json),
                created_at=row.created_at,
            )
            for row in rows
        ]
