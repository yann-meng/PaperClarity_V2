from fastapi import APIRouter

from schemas.common import ApiResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=ApiResponse)
def health() -> ApiResponse:
    return ApiResponse(data={"status": "ok"})
