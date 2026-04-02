from pydantic import BaseModel


class Section(BaseModel):
    id: str
    title: str
    level: int = 1
    start_block_id: str | None = None
    end_block_id: str | None = None
