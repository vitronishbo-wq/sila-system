- expurgar depois da analise de directorios vazados """
Pydantic schemas for QR signature validation endpoints.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional

class QRValidate(BaseModel):
    """Request schema for QR signature validation."""
    payload: str = Field(..., description="Original message/payload as base64 or hex string")
    signature: str = Field(..., description="Ed25519 signature as base64 string")
    public_key: str = Field(..., description="Ed25519 public key as base64 string")

    @validator('payload')
    def validate_payload(cls, v):
        # Basic check: ensure it's decodable
        import base64
        try:
            base64.b64decode(v)
            return v
        except:
            raise ValueError("Payload must be valid base64")

    @validator('signature', 'public_key')
    def validate_bytes(cls, v):
        import base64
        sig_bytes = base64.b64decode(v)
        if len(sig_bytes) != 64:  # Ed25519 signature size
            raise ValueError("Signature must be 64 bytes (Ed25519)")
        if len(sig_bytes) != 32:  # Ed25519 public key size for public_key
            raise ValueError("Public key must be 32 bytes (Ed25519)")
        return v

class ValidationResponse(BaseModel):
    """Response schema for signature validation."""
    valid: bool
    message: str = Field(..., description="Success/error message")

