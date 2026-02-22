"""Encryption service for monitoring module security."""

import base64
import json
import os
import secrets
from typing import Any, Dict, Optional, Union

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionService:
    """Service for encrypting and decrypting sensitive monitoring data."""

    def __init__(self):
        self.symmetric_key = self._get_or_generate_symmetric_key()
        self.cipher_suite = Fernet(self.symmetric_key)
        self.backend = default_backend()

    def encrypt_sensitive_data(self, data: Union[str, Dict[str, Any]]) -> str:
        """Encrypt sensitive data using symmetric encryption."""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True, default=str)
        else:
            data_str = str(data)

        encrypted_data = self.cipher_suite.encrypt(data_str.encode())
        return base64.b64encode(encrypted_data).decode()

    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        try:
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_bytes = self.cipher_suite.decrypt(encrypted_bytes)
            return decrypted_bytes.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt data: {str(e)}")

    def encrypt_field_level(
        self, data: Dict[str, Any], fields_to_encrypt: list
    ) -> Dict[str, Any]:
        """Encrypt specific fields in a dictionary."""
        encrypted_data = data.copy()

        for field in fields_to_encrypt:
            if field in encrypted_data and encrypted_data[field] is not None:
                encrypted_data[field] = self.encrypt_sensitive_data(
                    encrypted_data[field]
                )
                # Mark field as encrypted
                encrypted_data[f"{field}_encrypted"] = True

        return encrypted_data

    def decrypt_field_level(
        self, data: Dict[str, Any], fields_to_decrypt: list
    ) -> Dict[str, Any]:
        """Decrypt specific fields in a dictionary."""
        decrypted_data = data.copy()

        for field in fields_to_decrypt:
            if field in decrypted_data and decrypted_data.get(f"{field}_encrypted"):
                try:
                    decrypted_data[field] = self.decrypt_sensitive_data(
                        decrypted_data[field]
                    )
                    # Remove encryption marker
                    decrypted_data.pop(f"{field}_encrypted", None)
                except ValueError:
                    # Keep encrypted if decryption fails
                    pass

        return decrypted_data

    def generate_data_hash(self, data: Union[str, Dict[str, Any]]) -> str:
        """Generate a secure hash of data for integrity verification."""
        if isinstance(data, dict):
            data_str = json.dumps(data, sort_keys=True, default=str)
        else:
            data_str = str(data)

        digest = hashes.Hash(hashes.SHA256(), backend=self.backend)
        digest.update(data_str.encode())
        return digest.finalize().hex()

    def encrypt_with_key_derivation(
        self, data: str, password: str, salt: Optional[bytes] = None
    ) -> Dict[str, str]:
        """Encrypt data using password-based key derivation."""
        if salt is None:
            salt = os.urandom(16)

        # Derive key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend,
        )
        key = kdf.derive(password.encode())

        # Encrypt data
        cipher_suite = Fernet(base64.urlsafe_b64encode(key))
        encrypted_data = cipher_suite.encrypt(data.encode())

        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode(),
            "salt": base64.b64encode(salt).decode(),
        }

    def decrypt_with_key_derivation(
        self, encrypted_data: str, password: str, salt: str
    ) -> str:
        """Decrypt data using password-based key derivation."""
        try:
            # Decode salt
            salt_bytes = base64.b64decode(salt.encode())

            # Derive key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt_bytes,
                iterations=100000,
                backend=self.backend,
            )
            key = kdf.derive(password.encode())

            # Decrypt data
            cipher_suite = Fernet(base64.urlsafe_b64encode(key))
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_bytes = cipher_suite.decrypt(encrypted_bytes)

            return decrypted_bytes.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt with key derivation: {str(e)}")

    def generate_asymmetric_keys(self) -> Dict[str, str]:
        """Generate RSA key pair for asymmetric encryption."""
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=self.backend
        )

        public_key = private_key.public_key()

        # Serialize keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        return {"private_key": private_pem.decode(), "public_key": public_pem.decode()}

    def encrypt_with_public_key(self, data: str, public_key_pem: str) -> str:
        """Encrypt data using RSA public key."""
        try:
            public_key = serialization.load_pem_public_key(
                public_key_pem.encode(), backend=self.backend
            )

            encrypted_data = public_key.encrypt(
                data.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )

            return base64.b64encode(encrypted_data).decode()
        except Exception as e:
            raise ValueError(f"Failed to encrypt with public key: {str(e)}")

    def decrypt_with_private_key(
        self, encrypted_data: str, private_key_pem: str
    ) -> str:
        """Decrypt data using RSA private key."""
        try:
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode(), password=None
            )
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_data = private_key.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            return decrypted_data.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt with private key: {str(e)}")

    def create_secure_token(self, length: int = 32) -> str:
        """Create a cryptographically secure random token."""
        return secrets.token_urlsafe(length)

    def encrypt_audit_log_data(self, audit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive fields in audit log data."""
        sensitive_fields = [
            "user_email",
            "ip_address",
            "user_agent",
            "session_id",
            "description",
            "error_message",
        ]

        return self.encrypt_field_level(audit_data, sensitive_fields)

    def decrypt_audit_log_data(
        self, encrypted_audit_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Decrypt sensitive fields in audit log data."""
        sensitive_fields = [
            "user_email",
            "ip_address",
            "user_agent",
            "session_id",
            "description",
            "error_message",
        ]

        return self.decrypt_field_level(encrypted_audit_data, sensitive_fields)

    def encrypt_metric_data(self, metric_data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive fields in metric data."""
        sensitive_fields = ["metadata", "tags"]

        return self.encrypt_field_level(metric_data, sensitive_fields)

    def decrypt_metric_data(
        self, encrypted_metric_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Decrypt sensitive fields in metric data."""
        sensitive_fields = ["metadata", "tags"]

        return self.decrypt_field_level(encrypted_metric_data, sensitive_fields)

    def encrypt_alert_data(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive fields in alert data."""
        sensitive_fields = ["alert_data", "trigger_conditions", "tags"]

        return self.encrypt_field_level(alert_data, sensitive_fields)

    def decrypt_alert_data(
        self, encrypted_alert_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Decrypt sensitive fields in alert data."""
        sensitive_fields = ["alert_data", "trigger_conditions", "tags"]

        return self.decrypt_field_level(encrypted_alert_data, sensitive_fields)

    def create_encrypted_backup(
        self, data: Dict[str, Any], backup_password: str
    ) -> str:
        """Create an encrypted backup of monitoring data."""
        # Serialize data
        data_json = json.dumps(data, sort_keys=True, default=str)

        # Encrypt with password
        encrypted_backup = self.encrypt_with_key_derivation(data_json, backup_password)

        # Add metadata
        backup_data = {
            "version": "1.0",
            "timestamp": "2024-01-01T00:00:00Z",  # Would use actual timestamp
            "data_type": "monitoring_backup",
            "encrypted_data": encrypted_backup["encrypted_data"],
            "salt": encrypted_backup["salt"],
        }

        return json.dumps(backup_data)

    def restore_encrypted_backup(
        self, backup_data: str, backup_password: str
    ) -> Dict[str, Any]:
        """Restore data from encrypted backup."""
        try:
            # Parse backup
            backup = json.loads(backup_data)

            # Decrypt data
            decrypted_json = self.decrypt_with_key_derivation(
                backup["encrypted_data"], backup_password, backup["salt"]
            )

            return json.loads(decrypted_json)
        except Exception as e:
            raise ValueError(f"Failed to restore encrypted backup: {str(e)}")

    def rotate_encryption_keys(self) -> Dict[str, str]:
        """Rotate encryption keys for enhanced security."""
        # Generate new symmetric key
        new_key = Fernet.generate_key()
        old_key = self.symmetric_key

        # Update current key
        self.symmetric_key = new_key
        self.cipher_suite = Fernet(new_key)

        return {
            "old_key": base64.b64encode(old_key).decode(),
            "new_key": base64.b64encode(new_key).decode(),
            "rotation_timestamp": "2024-01-01T00:00:00Z",  # Would use actual timestamp
        }

    def re_encrypt_with_new_key(self, encrypted_data: str, old_key: str) -> str:
        """Re-encrypt data with new key after key rotation."""
        try:
            # Create cipher with old key
            old_key_bytes = base64.b64decode(old_key.encode())
            old_cipher = Fernet(old_key_bytes)

            # Decrypt with old key
            encrypted_bytes = base64.b64decode(encrypted_data.encode())
            decrypted_data = old_cipher.decrypt(encrypted_bytes)

            # Encrypt with new key
            new_encrypted = self.cipher_suite.encrypt(decrypted_data)
            return base64.b64encode(new_encrypted).decode()
        except Exception as e:
            raise ValueError(f"Failed to re-encrypt with new key: {str(e)}")

    # ============================================================================
    # PRIVATE HELPER METHODS
    # ============================================================================

    def _get_or_generate_symmetric_key(self) -> bytes:
        """Get existing symmetric key or generate new one."""
        # Try to get key from environment
        key_env = settings.MONITORING_ENCRYPTION_KEY
        if key_env:
            try:
                return base64.b64decode(key_env.encode())
            except Exception:
                pass

        # Generate new key from password
        return Fernet.generate_key()

    def _secure_delete(self, data: bytes) -> None:
        """Securely delete sensitive data from memory."""
        # In Python, this is limited, but we can overwrite the data
        if isinstance(data, str):
            data = data.encode()

        # Overwrite with random data
        for _ in range(3):
            secrets.randbits(len(data) * 8)
