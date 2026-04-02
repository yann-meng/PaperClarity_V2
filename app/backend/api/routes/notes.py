from fastapi import APIRouter, Depends
from sqlmodel import Session

from db.engine import get_session
from db.repositories.note_repo import NoteRepository
from models.note import NoteCreate
from schemas.common import ApiResponse

router = APIRouter(prefix="/notes", tags=["notes"])
repo = NoteRepository()


@router.post("", response_model=ApiResponse)
def create_note(payload: NoteCreate, session: Session = Depends(get_session)) -> ApiResponse:
    note = repo.create(session, payload)
    return ApiResponse(data=note.model_dump())


@router.get("/{doc_id}", response_model=ApiResponse)
def list_notes(doc_id: str, session: Session = Depends(get_session)) -> ApiResponse:
    notes = repo.list_by_document(session, doc_id)
    return ApiResponse(data=[n.model_dump() for n in notes])
