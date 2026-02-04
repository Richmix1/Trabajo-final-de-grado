from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

import httpx

from app.core.config import settings
from app.models.schemas import Priority, TaskAISuggestRequest, TaskAISuggestResponse


KEYWORD_PRIORITY = {
    "urgente": Priority.alta,
    "asap": Priority.alta,
    "hoy": Priority.alta,
    "inmediato": Priority.alta,
    "mañana": Priority.media,
    "proximo": Priority.media,
}


def _heuristic_priority(payload: TaskAISuggestRequest) -> Priority:
    title = payload.title.lower()
    for keyword, priority in KEYWORD_PRIORITY.items():
        if keyword in title:
            return priority

    if payload.due_date:
        now = datetime.utcnow()
        if payload.due_date <= now + timedelta(days=3):
            return Priority.alta
        if payload.due_date <= now + timedelta(days=7):
            return Priority.media
        return Priority.baja

    return Priority.media


def _fallback_description(payload: TaskAISuggestRequest, priority: Priority) -> str:
    base = (payload.description or "").strip()
    steps = [
        "1. Define el resultado esperado.",
        "2. Enumera los recursos necesarios.",
        "3. Divide el trabajo en subtareas pequeñas.",
        "4. Estima tiempos y bloquea huecos en el calendario.",
        "5. Revisa el progreso y ajusta si es necesario.",
    ]
    summary = (
        f"Prioridad sugerida: {priority.value}. Tarea: {payload.title}. "
        "Sugerencia de enfoque:\n" + "\n".join(steps)
    )
    if base:
        return f"{base}\n\n{summary}"
    return summary


def _build_prompt(payload: TaskAISuggestRequest) -> str:
    due = payload.due_date.isoformat() if payload.due_date else "No definida"
    return (
        "Eres un asistente para gestión de tareas.\n"
        "Genera una descripción mejorada con pasos concretos y sugiere la prioridad "
        "(ALTA/MEDIA/BAJA) basada en urgencia, fecha límite y palabras clave.\n"
        f"Título: {payload.title}\n"
        f"Descripción actual: {payload.description or 'N/A'}\n"
        f"Fecha límite: {due}\n"
        "Responde en JSON con las claves description_generated y priority_suggested."
    )


async def suggest_with_ai(payload: TaskAISuggestRequest) -> TaskAISuggestResponse:
    priority = _heuristic_priority(payload)
    if not settings.ai_enabled or not settings.ai_api_key:
        return TaskAISuggestResponse(
            priority_suggested=priority,
            description_generated=_fallback_description(payload, priority),
        )

    base_url = settings.ai_base_url or "https://api.openai.com/v1"
    model = settings.ai_model or "gpt-4o-mini"
    prompt = _build_prompt(payload)

    headers = {
        "Authorization": f"Bearer {settings.ai_api_key}",
        "Content-Type": "application/json",
    }
    request_body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Asistente de gestión de tareas."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(f"{base_url.rstrip('/')}/chat/completions", json=request_body, headers=headers)
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPError, ValueError):
        return TaskAISuggestResponse(
            priority_suggested=priority,
            description_generated=_fallback_description(payload, priority),
        )

    ai_text: Optional[str] = None
    try:
        ai_text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        ai_text = None

    if not ai_text:
        return TaskAISuggestResponse(
            priority_suggested=priority,
            description_generated=_fallback_description(payload, priority),
        )

    try:
        parsed = httpx.Response(200, content=ai_text).json()
        description = parsed.get("description_generated")
        priority_value = parsed.get("priority_suggested")
        if description and priority_value in {p.value for p in Priority}:
            return TaskAISuggestResponse(
                priority_suggested=Priority(priority_value),
                description_generated=description,
            )
    except ValueError:
        pass

    return TaskAISuggestResponse(
        priority_suggested=priority,
        description_generated=_fallback_description(payload, priority),
    )
