"""
QR Signature Validation Endpoint for Identity module.
"""

from fastapi import APIRouter, HTTPException, status

from apps.backend.app.modules.identity.api.schemas.qr import QRValidate, ValidationResponse
from apps.backend.app.modules.identity.domain.services.qr_signature_validator import (
    InvalidSignatureError,
    QRSignatureValidator,
)

router = APIRouter(prefix="/validate-qr", tags=["identity-qr"])

current_user_dep = Depends(get_current_user)


@router.post("/", response_model=ValidationResponse, status_code=status.HTTP_200_OK)
async def validate_qr_signature(
    request: QRValidate,
    # current_user=current_user_dep  # Uncomment if auth required
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
            valid=is_valid, message="Signature valid" if is_valid else "Signature invalid"
        )

    except InvalidSignatureError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation error: {str(e)}",
        ) from e
