from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# ---------------------------
# Journey Schemas
# ---------------------------


class JourneyBase(BaseModel):
    citizen_id: int
    title: str
    description: Optional[str] = None
    status: str = "active"


class JourneyCreate(JourneyBase):
    start_date: Optional[datetime] = None


class JourneyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Journey(JourneyBase):
    id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Journey Step Schemas
# ---------------------------


class JourneyStepBase(BaseModel):
    journey_id: int
    title: str
    description: Optional[str] = None
    status: str = "pending"
    order: int
    estimated_duration: Optional[int] = None


class JourneyStepCreate(JourneyStepBase):
    pass


class JourneyStepUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    order: Optional[int] = None
    estimated_duration: Optional[int] = None
    actual_duration: Optional[int] = None


class JourneyStep(JourneyStepBase):
    id: int
    actual_duration: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------------------------
# Journey with Steps
# ---------------------------


class JourneyWithSteps(Journey):
    steps: List[JourneyStep] = []

    model_config = ConfigDict(from_attributes=True)
