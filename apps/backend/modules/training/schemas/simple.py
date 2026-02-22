"""Minimal Training schemas (Pydantic v2) used by training routes."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TrainingModuleCreate(BaseModel):
    module_name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_duration: Optional[int] = None


class TrainingModuleRead(TrainingModuleCreate):
    id: int
    is_active: bool = True
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TrainingUserCreate(BaseModel):
    user_name: str


class TrainingUserRead(TrainingUserCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TrainingSessionCreate(BaseModel):
    user_name: str
    training_module: str
    session_type: Optional[str] = None
    difficulty_level: Optional[str] = None


class TrainingSessionRead(BaseModel):
    id: int
    user_name: str
    training_module: str
    session_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    status: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    completion_score: Optional[int] = None
    feedback: Optional[str] = None
    duration_minutes: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
