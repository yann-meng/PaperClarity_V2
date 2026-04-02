from sqlmodel import Session

from db.repositories.document_repo import DocumentRepository
from models.document import Document
from services.document_loader import detect_doc_type
from services.pdf_parser import PdfParser


class DocumentService:
    def __init__(self) -> None:
        self.repo = DocumentRepository()
        self.pdf_parser = PdfParser()

    def load(self, session: Session, file_path: str) -> Document:
        doc_type = detect_doc_type(file_path)
        if doc_type != "pdf":
            raise ValueError(f"Unsupported doc type: {doc_type}")
        document = self.pdf_parser.parse(file_path)
        self.repo.upsert_document(session, document)
        return document

    def get(self, session: Session, document_id: str) -> Document | None:
        return self.repo.get_document(session, document_id)
