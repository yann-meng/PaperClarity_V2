from pydantic import BaseModel


class Equation(BaseModel):
    id: str
    page: int
    raw_text: str
    latex: str | None = None
    block_id: str
    symbols: dict[str, str] = {}
