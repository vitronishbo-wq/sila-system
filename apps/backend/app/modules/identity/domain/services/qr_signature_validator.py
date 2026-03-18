"""
QR Signature Validator Service for Identity module.

Uses cryptography library for Ed25519 signature verification.
"""
from typing import Union
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

from apps.backend.app.modules.identity.domain.exceptions import DomainException, DomainExceptionFactory

class InvalidSignatureError(DomainException):
    """Raised when Ed25519 signature verification fails."""
    code = "INVALID_QR_SIGNATURE"

class QRSignatureValidator:
    """
    Service for verifying Ed25519 signatures in QR payloads.
    """
    
    @staticmethod
    def verify_signature(
        payload: bytes, 
        signature: bytes, 
        public_key: bytes
    ) -> bool:
        """
        Verify Ed25519 signature against payload using public key.
        
        :param payload: Original message bytes
        :param signature: Ed25519 signature bytes (64 bytes)
        :param public_key: Ed25519 public key bytes (32 bytes)
        :return: True if valid, raises InvalidSignatureError if not
        """
        try:
            public_key_obj = ed25519.Ed25519PublicKey.from_public_bytes(public_key)
            public_key_obj.verify(signature, payload)
            return True
        except InvalidSignature as e:
            raise InvalidSignatureError(f"Signature verification failed: {str(e)}") from e
        except Exception as e:
            raise DomainExceptionFactory.invalid_argument(f"Invalid signature/public_key format: {str(e)}") from e

