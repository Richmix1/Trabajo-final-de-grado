from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.core.config import settings
from app.core.security import get_current_user
from app.models.schemas import Priority, TaskAISuggestRequest, TaskAISuggestResponse

router = APIRouter(prefix="/tasks/ai", tags=["ai"])


def _heuristic_priority(payload: TaskAISuggestRequest) -> Priority:
    title = payload.title.lower()
    if any(keyword in title for keyword in ["urgente", "asap", "hoy", "inmediato"]):
        return Priority.alta

    if payload.due_date:
        now = datetime.utcnow()
        if payload.due_date <= now + timedelta(days=3):
            return Priority.alta
        if payload.due_date <= now + timedelta(days=7):
            return Priority.media
        return Priority.baja

    return Priority.media


def _generate_description(payload: TaskAISuggestRequest, priority: Priority) -> str:
    base = payload.description or ""
    if base:
        return base
    return (
        f"Prioridad sugerida {priority.value}. "
        f"Describe los pasos clave para completar: {payload.title}."
    )


@router.post("/suggest", response_model=TaskAISuggestResponse)
async def suggest_task(
    payload: TaskAISuggestRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> TaskAISuggestResponse:
    _ = current_user
    if settings.ai_key:
        priority = _heuristic_priority(payload)
        description = _generate_description(payload, priority)
        return TaskAISuggestResponse(priority_suggested=priority, description_generated=description)

    priority = _heuristic_priority(payload)
    description = _generate_description(payload, priority)
    return TaskAISuggestResponse(priority_suggested=priority, description_generated=description)
