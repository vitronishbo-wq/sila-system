from dataclasses import asdict
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from foundation.eligibility.engine import EligibilityEngine
from foundation.eligibility.evaluator import Evaluator

router = APIRouter()


class TransferBody(BaseModel):
    student_id: str
    target_school: str
    target_class: str | None
    academic_year: str
    date_of_birth: str | None = None
    debts: list[dict[str, Any]] | None = None
    sanctions: list[str] | None = None
    institution_capacity: dict[str, Any] | None = None
    vacancies: int | None = None
    metadata: dict[str, Any] | None = None


@router.post("/educacao/eligibility/transfer")
def post_transfer(body: TransferBody):
    """Evaluate a transfer request and optionally execute it automatically."""
    evaluator = Evaluator()
    engine = EligibilityEngine(evaluator)

    req = body.dict()

    try:
        result = engine.evaluate_transfer(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # If result is a dataclass (TransferResult), convert to dict
    try:
        return asdict(result)
    except Exception:
        # Otherwise assume it's already serializable
        return result
