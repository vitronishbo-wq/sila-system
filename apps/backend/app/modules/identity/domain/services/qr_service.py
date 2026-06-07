import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import ed25519


class QRVerificationService:
    @staticmethod
    def verify_identity_qr(payload_json: str, signature_hex: str, public_key_hex: str) -> bool:
        """
        Verifica se o payload do BI Digital foi assinado pela chave privada correspondente.
        """
        try:
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(public_key_hex))
            signature = bytes.fromhex(signature_hex)
            data = payload_json.encode("utf-8")

            public_key.verify(signature, data)
            return True
        except (InvalidSignature, ValueError, TypeError):
            return False

    @staticmethod
    def decode_qr_payload(payload_json: str):
        return json.loads(payload_json)
