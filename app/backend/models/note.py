from datetime import datetime

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    document_id: str
    title: str
    content: str
    citations: list[dict] = Field(default_factory=list)


class Note(BaseModel):
    id: int
    document_id: str
    title: str
    content: str
    citations: list[dict] = Field(default_factory=list)
    created_at: datetime
