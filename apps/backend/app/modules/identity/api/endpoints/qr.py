from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ....domain.services.qr_service import QRVerificationService

router = APIRouter(prefix="/qr", tags=["QR Validation"])


class QRValidationRequest(BaseModel):
    payload: str  # JSON string do frontend
    signature: str  # hex
    citizen_did: str
    public_key: str  # hex (for simplicity, from frontend/DB)


@router.post("/validate-qr")
async def validate_citizen_qr(request: QRValidationRequest):
    # Fetch pubkey from repo if needed
    # pub_key = await identity_repo.get_pub_key(request.citizen_did)

    is_valid = QRVerificationService.verify_identity_qr(
        request.payload, request.signature, request.public_key
    )

    if not is_valid:
        raise HTTPException(status_code=400, detail="Assinatura digital inválida ou QR expirado")

    data = QRVerificationService.decode_qr_payload(request.payload)
    return {"status": "verified", "data": data, "timestamp": "2024-01-01T00:00:00Z"}
