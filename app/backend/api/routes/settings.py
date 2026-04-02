from fastapi import APIRouter
from pydantic import BaseModel

from core.config import settings
from schemas.common import ApiResponse

router = APIRouter(prefix="/settings", tags=["settings"])


class LLMSettings(BaseModel):
    llm_provider: str
    llm_base_url: str
    llm_model: str


@router.get("/llm", response_model=ApiResponse)
def get_llm_settings() -> ApiResponse:
    return ApiResponse(
        data={
            "llm_provider": settings.llm_provider,
            "llm_base_url": settings.llm_base_url,
            "llm_model": settings.llm_model,
        }
    )


@router.post("/llm", response_model=ApiResponse)
def set_llm_settings(payload: LLMSettings) -> ApiResponse:
    return ApiResponse(data=payload.model_dump())
