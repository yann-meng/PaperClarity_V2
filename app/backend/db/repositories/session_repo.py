import json
from datetime import datetime

from sqlmodel import Session, select

from db.tables import SessionTable
from models.session import ChatSession, ChatTurn


class SessionRepository:
    def get_by_document(self, session: Session, document_id: str) -> ChatSession | None:
        row = session.exec(select(SessionTable).where(SessionTable.document_id == document_id)).first()
        if row is None:
            return None
        turns_payload = json.loads(row.turns_json)
        turns = [ChatTurn(**turn) for turn in turns_payload]
        return ChatSession(id=row.id or 0, document_id=row.document_id, turns=turns, updated_at=row.updated_at)

    def append_turn(self, session: Session, document_id: str, role: str, content: str) -> ChatSession:
        row = session.exec(select(SessionTable).where(SessionTable.document_id == document_id)).first()
        turns = []
        if row is None:
            row = SessionTable(document_id=document_id)
            session.add(row)
        else:
            turns = json.loads(row.turns_json)
        turns.append({"role": role, "content": content, "created_at": datetime.utcnow().isoformat()})
        row.turns_json = json.dumps(turns, ensure_ascii=False)
        row.updated_at = datetime.utcnow()
        session.commit()
        session.refresh(row)
        chat_turns = [ChatTurn(role=t["role"], content=t["content"], created_at=datetime.fromisoformat(t["created_at"])) for t in turns]
        return ChatSession(id=row.id or 0, document_id=document_id, turns=chat_turns, updated_at=row.updated_at)
