from datetime import datetime

from sqlmodel import Field, SQLModel


class DocumentTable(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    source_path: str
    doc_type: str = "pdf"
    metadata_json: str = "{}"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BlockTable(SQLModel, table=True):
    id: str = Field(primary_key=True)
    document_id: str = Field(index=True)
    page: int
    section_id: str | None = None
    block_type: str
    text: str
    bbox_json: str = "[]"
    order: int


class SectionTable(SQLModel, table=True):
    id: str = Field(primary_key=True)
    document_id: str = Field(index=True)
    title: str
    level: int = 1
    start_block_id: str | None = None
    end_block_id: str | None = None


class EquationTable(SQLModel, table=True):
    id: str = Field(primary_key=True)
    document_id: str = Field(index=True)
    page: int
    raw_text: str
    latex: str | None = None
    block_id: str
    symbols_json: str = "{}"


class NoteTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    document_id: str = Field(index=True)
    title: str
    content: str
    citations_json: str = "[]"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SessionTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    document_id: str = Field(index=True)
    turns_json: str = "[]"
    updated_at: datetime = Field(default_factory=datetime.utcnow)
