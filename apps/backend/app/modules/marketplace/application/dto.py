from __future__ import annotations

from typing import Any, Dict, Optional
from pydantic import BaseModel


class StudentProfileDTO(BaseModel):
    age: Optional[int] = 18
    academic_performance: Optional[float] = 0.0
    special_needs: Optional[list[str]] = []
    location: Optional[dict] = {}
    available_budget: Optional[float] = 0.0
    previous_transfers: Optional[int] = 0


class InstantTransferRequestDTO(BaseModel):
    student_id: str
    student_profile: Optional[StudentProfileDTO] = None
    preferred_institution_id: Optional[str] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class StepResultDTO(BaseModel):
    status: str
    detail: Optional[Dict[str, Any]] = None


class InstantTransferResponseDTO(BaseModel):
    status: str
    transfer_id: Optional[str] = None
    transaction_id: str
    steps: Dict[str, StepResultDTO]
