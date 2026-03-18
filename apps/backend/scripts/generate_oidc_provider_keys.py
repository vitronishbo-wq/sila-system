from __future__ import annotations

from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def main() -> None:
    backend_root = Path(__file__).resolve().parents[1]
    key_dir = backend_root / ".secrets" / "oidc"
    key_dir.mkdir(parents=True, exist_ok=True)

    private_path = key_dir / "oidc_provider_private.pem"
    public_path = key_dir / "oidc_provider_public.pem"

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    private_path.write_bytes(private_pem)
    public_path.write_bytes(public_pem)

    print(f"Generated OIDC provider keypair in {key_dir}")
    print("Set these environment variables:")
    print(f"OIDC_PROVIDER_PRIVATE_KEY_PATH={private_path}")
    print(f"OIDC_PROVIDER_PUBLIC_KEY_PATH={public_path}")


if __name__ == "__main__":
    main()
