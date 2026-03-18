"""
Biometric enrollment endpoint for Identity module.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status

from apps.backend.app.modules.identity.api.schemas.biometrics import (
    BiometricEnrollRequest,
    BiometricEnrollResponse,
)

router = APIRouter(prefix="/citizens/{citizen_id}/biometric", tags=["identity-biometrics"])


@router.post("/enroll", response_model=BiometricEnrollResponse, status_code=status.HTTP_201_CREATED)
async def enroll_biometric(citizen_id: str, request: BiometricEnrollRequest) -> BiometricEnrollResponse:
    """
    Recebe o template biométrico do frontend e valida a qualidade mínima.
    """
    if citizen_id != request.citizen_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="citizen_id no path difere do payload",
        )

    threshold = request.quality_threshold if request.quality_threshold is not None else 70.0
    if request.quality_score < threshold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Qualidade biométrica insuficiente para registro (Mínimo {threshold:.0f}%)",
        )

    return BiometricEnrollResponse(
        id=f"bio_tmp_{citizen_id[:8]}",
        citizen_id=citizen_id,
        status="ENROLLED",
        created_at=datetime.utcnow(),
    )
