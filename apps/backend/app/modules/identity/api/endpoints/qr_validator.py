"""
QR Signature Validation Endpoint for Identity module.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from apps.backend.app.api.dependencies import get_current_user
from apps.backend.app.modules.identity.api.schemas.qr import QRValidate, ValidationResponse
from apps.backend.app.modules.identity.domain.services.qr_signature_validator import (
    QRSignatureValidator, InvalidSignatureError
)

router = APIRouter(prefix="/validate-qr", tags=["identity-qr"])

@router.post("/", response_model=ValidationResponse, status_code=status.HTTP_200_OK)
async def validate_qr_signature(
    request: QRValidate,
    # current_user=Depends(get_current_user)  # Uncomment if auth required
) -> ValidationResponse:
    """
    Validate Ed25519 signature in QR payload.
    """
    try:
        # Decode base64 strings to bytes
        import base64
        payload_bytes = base64.b64decode(request.payload)
        signature_bytes = base64.b64decode(request.signature)
        public_key_bytes = base64.b64decode(request.public_key)
        
        # Verify signature
        is_valid = QRSignatureValidator.verify_signature(
            payload_bytes, signature_bytes, public_key_bytes
        )
        
        return ValidationResponse(
            valid=is_valid,
            message="Signature valid" if is_valid else "Signature invalid"
        )
    
    except InvalidSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation error: {str(e)}"
        )

