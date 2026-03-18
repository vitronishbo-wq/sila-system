"""
Unit tests for QR signature validator.
"""
import pytest
import base64
from cryptography.hazmat.primitives.asymmetric import ed25519
from apps.backend.app.modules.identity.domain.services.qr_signature_validator import (
    QRSignatureValidator, InvalidSignatureError
)

@pytest.fixture
def valid_keypair():
    """Generate valid Ed25519 keypair."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

@pytest.fixture
def test_payload():
    """Test message payload."""
    return b"QR test message: user biometric data"

class TestQRSignatureValidator:
    
    def test_valid_signature(self, valid_keypair, test_payload):
        """Test valid signature verification."""
        private_key, public_key = valid_keypair
        signature = private_key.sign(test_payload)
        
        pub_b64 = base64.b64encode(public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )).decode()
        sig_b64 = base64.b64encode(signature).decode()
        
        # Service expects bytes, but test direct
        is_valid = QRSignatureValidator.verify_signature(
            test_payload, signature, public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
        )
        assert is_valid is True
    
    def test_invalid_signature(self, valid_keypair, test_payload):
        """Test invalid signature."""
        private_key, public_key = valid_keypair
        # Wrong signature (sign different payload)
        wrong_signature = private_key.sign(b"wrong payload")
        
        with pytest.raises(InvalidSignatureError):
            QRSignatureValidator.verify_signature(
                test_payload, wrong_signature, public_key.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw
                )
            )
    
    def test_invalid_public_key_length(self, valid_keypair, test_payload):
        """Test invalid public key length."""
        _, public_key = valid_keypair
        short_key = b"too-short"
        
        with pytest.raises(Exception):  # DomainExceptionFactory.invalid_argument
            QRSignatureValidator.verify_signature(
                test_payload, b"signature", short_key
            )
    
    def test_invalid_signature_length(self, valid_keypair, test_payload):
        """Test invalid signature length."""
        _, public_key = valid_keypair
        short_sig = b"too-short"
        
        with pytest.raises(Exception):  # Crypto exception wrapped
            QRSignatureValidator.verify_signature(
                test_payload, short_sig, public_key.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw
                )
            )

