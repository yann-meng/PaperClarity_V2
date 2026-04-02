from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from db.engine import get_session
from db.repositories.document_repo import DocumentRepository
from schemas.common import ApiResponse
from services.context_service import ContextService
from services.llm_gateway import LLMGateway
from skills.loader import load_skills
from skills.registry import SkillRegistry

router = APIRouter(prefix="/skills", tags=["skills"])
registry = SkillRegistry()
load_skills(registry)
context_service = ContextService()
llm = LLMGateway()
doc_repo = DocumentRepository()


class RunSkillRequest(BaseModel):
    document_id: str
    context_type: str = "paper"
    selected_block_ids: list[str] = []
    selected_equation_id: str | None = None
    user_input: str | None = None


@router.get("", response_model=ApiResponse)
def list_skills() -> ApiResponse:
    data = [
        {
            "name": skill.name,
            "display_name": skill.display_name,
            "description": skill.description,
            "supported_contexts": skill.supported_contexts,
        }
        for skill in registry.list_all()
    ]
    return ApiResponse(data=data)


@router.post("/{skill_name}/run", response_model=ApiResponse)
def run_skill(skill_name: str, payload: RunSkillRequest, session: Session = Depends(get_session)) -> ApiResponse:
    if skill_name not in [s.name for s in registry.list_all()]:
        raise HTTPException(status_code=404, detail="Skill not found")
    document = doc_repo.get_document(session, payload.document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    if payload.context_type == "paper":
        context = context_service.build_paper_context(document)
    elif payload.context_type == "paragraph":
        context = context_service.build_paragraph_context(document, payload.selected_block_ids)
    elif payload.context_type == "equation" and payload.selected_equation_id:
        context = context_service.build_equation_context(document, payload.selected_equation_id)
    elif payload.context_type == "experiment":
        context = context_service.build_experiment_context(document)
    else:
        context = context_service.build_paper_context(document)

    skill = registry.get(skill_name)
    try:
        result = skill.run(context=context, llm_client=llm, user_input=payload.user_input)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ApiResponse(data=result)
