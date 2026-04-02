from pydantic import BaseModel


class Block(BaseModel):
    id: str
    page: int
    section_id: str | None = None
    block_type: str = "paragraph"
    text: str
    bbox: list[float] | None = None
    order: int
