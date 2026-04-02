from pydantic import BaseModel, Field

from models.block import Block
from models.equation import Equation
from models.section import Section


class Document(BaseModel):
    id: str
    title: str
    source_path: str
    doc_type: str = "pdf"
    metadata: dict = Field(default_factory=dict)
    sections: list[Section] = Field(default_factory=list)
    blocks: list[Block] = Field(default_factory=list)
    figures: list[dict] = Field(default_factory=list)
    tables: list[dict] = Field(default_factory=list)
    equations: list[Equation] = Field(default_factory=list)
