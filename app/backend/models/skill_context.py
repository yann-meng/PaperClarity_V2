from pydantic import BaseModel, Field


class SkillContext(BaseModel):
    document_id: str
    context_type: str
    selected_block_ids: list[str] = Field(default_factory=list)
    selected_equation_id: str | None = None
    user_note: str | None = None
    extra_context: dict = Field(default_factory=dict)
