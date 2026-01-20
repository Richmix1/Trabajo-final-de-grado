from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserLogin(UserBase):
    password: str


class UserPublic(UserBase):
    id: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None


class Priority(str, Enum):
    alta = "ALTA"
    media = "MEDIA"
    baja = "BAJA"


class Status(str, Enum):
    pendiente = "PENDIENTE"
    en_progreso = "EN_PROGRESO"
    completada = "COMPLETADA"


class TaskBase(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    priority: Priority = Priority.media
    status: Status = Status.pendiente
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[Status] = None
    due_date: Optional[datetime] = None


class TaskPublic(TaskBase):
    id: str
    user_id: str
    created_at: datetime


class TaskAISuggestRequest(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskAISuggestResponse(BaseModel):
    priority_suggested: Priority
    description_generated: str
