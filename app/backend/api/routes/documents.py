from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from db.engine import get_session
from db.repositories.document_repo import DocumentRepository
from schemas.common import ApiResponse
from services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["documents"])
service = DocumentService()
repo = DocumentRepository()


class LoadDocumentRequest(BaseModel):
    file_path: str


@router.post("/load", response_model=ApiResponse)
def load_document(payload: LoadDocumentRequest, session: Session = Depends(get_session)) -> ApiResponse:
    try:
        document = service.load(session=session, file_path=payload.file_path)
        return ApiResponse(data=document.model_dump())
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{doc_id}", response_model=ApiResponse)
def get_document(doc_id: str, session: Session = Depends(get_session)) -> ApiResponse:
    document = repo.get_document(session, doc_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return ApiResponse(data=document.model_dump())


@router.get("/{doc_id}/blocks", response_model=ApiResponse)
def get_document_blocks(doc_id: str, session: Session = Depends(get_session)) -> ApiResponse:
    document = repo.get_document(session, doc_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return ApiResponse(data=[block.model_dump() for block in document.blocks])


@router.get("/{doc_id}/sections", response_model=ApiResponse)
def get_document_sections(doc_id: str, session: Session = Depends(get_session)) -> ApiResponse:
    document = repo.get_document(session, doc_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return ApiResponse(data=[section.model_dump() for section in document.sections])


@router.get("/{doc_id}/equations", response_model=ApiResponse)
def get_document_equations(doc_id: str, session: Session = Depends(get_session)) -> ApiResponse:
    document = repo.get_document(session, doc_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return ApiResponse(data=[equation.model_dump() for equation in document.equations])
