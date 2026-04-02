from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from db.engine import get_session
from db.repositories.document_repo import DocumentRepository
from db.repositories.note_repo import NoteRepository
from schemas.common import ApiResponse
from services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["export"])
doc_repo = DocumentRepository()
note_repo = NoteRepository()
export_service = ExportService()


class ExportMarkdownRequest(BaseModel):
    document_id: str


@router.post("/markdown", response_model=ApiResponse)
def export_markdown(payload: ExportMarkdownRequest, session: Session = Depends(get_session)) -> ApiResponse:
    document = doc_repo.get_document(session, payload.document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    notes = note_repo.list_by_document(session, payload.document_id)
    markdown = export_service.notes_to_markdown(document.title, notes)
    return ApiResponse(data={"markdown": markdown})
