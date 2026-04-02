from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.engine import get_session
from db.repositories.session_repo import SessionRepository
from schemas.common import ApiResponse

router = APIRouter(prefix="/sessions", tags=["sessions"])
repo = SessionRepository()


@router.get("/{doc_id}", response_model=ApiResponse)
def get_session_by_doc(doc_id: str, session: Session = Depends(get_session)) -> ApiResponse:
    item = repo.get_by_document(session, doc_id)
    return ApiResponse(data=item.model_dump() if item else {"document_id": doc_id, "turns": []})
