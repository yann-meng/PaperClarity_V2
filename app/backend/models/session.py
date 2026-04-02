from datetime import datetime

from pydantic import BaseModel, Field


class ChatTurn(BaseModel):
    role: str
    content: str
    created_at: datetime


class ChatSession(BaseModel):
    id: int
    document_id: str
    turns: list[ChatTurn] = Field(default_factory=list)
    updated_at: datetime
