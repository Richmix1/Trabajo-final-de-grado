from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.schemas import TaskAISuggestRequest, TaskAISuggestResponse
from app.services.ai import suggest_with_ai

router = APIRouter(prefix="/tasks/ai", tags=["ai"])


@router.post("/suggest", response_model=TaskAISuggestResponse)
async def suggest_task(
    payload: TaskAISuggestRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> TaskAISuggestResponse:
    _ = current_user
    return await suggest_with_ai(payload)
