from datetime import datetime
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.db.mongo import get_database
from app.models.schemas import TaskCreate, TaskPublic, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _serialize_task(task: Dict[str, Any]) -> TaskPublic:
    return TaskPublic(
        id=task["_id"],
        user_id=task["user_id"],
        title=task["title"],
        description=task.get("description"),
        priority=task["priority"],
        status=task["status"],
        due_date=task.get("due_date"),
        created_at=task["created_at"],
    )


@router.get("", response_model=List[TaskPublic])
async def list_tasks(current_user: Dict[str, Any] = Depends(get_current_user)) -> List[TaskPublic]:
    db = get_database()
    cursor = db.tasks.find({"user_id": current_user["_id"]})
    tasks = await cursor.to_list(length=200)
    return [_serialize_task(task) for task in tasks]


@router.post("", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> TaskPublic:
    db = get_database()
    task_id = str(uuid4())
    task_doc = {
        "_id": task_id,
        "user_id": current_user["_id"],
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority,
        "status": payload.status,
        "due_date": payload.due_date,
        "created_at": datetime.utcnow(),
    }
    await db.tasks.insert_one(task_doc)
    return _serialize_task(task_doc)


@router.put("/{task_id}", response_model=TaskPublic)
async def update_task(
    task_id: str,
    payload: TaskUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> TaskPublic:
    db = get_database()
    task = await db.tasks.find_one({"_id": task_id, "user_id": current_user["_id"]})
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = payload.dict(exclude_unset=True)
    if update_data:
        await db.tasks.update_one(
            {"_id": task_id, "user_id": current_user["_id"]},
            {"$set": update_data},
        )
        task.update(update_data)

    return _serialize_task(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> None:
    db = get_database()
    result = await db.tasks.delete_one({"_id": task_id, "user_id": current_user["_id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
