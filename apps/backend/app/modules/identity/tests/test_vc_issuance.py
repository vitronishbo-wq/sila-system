import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from apps.backend.app.modules.identity.verifiable_credentials.domain.entities.credential import VerifiableCredential
from apps.backend.app.modules.identity.verifiable_credentials.application.services.credential_signer import CredentialSigner

def test_vc_issuance_and_signature_flow():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    vc = VerifiableCredential(
        id="http://sila.gov.ao/credentials/test-001",
        issuer="did:sila:gov:registry",
        credential_subject={"name": "Cidadão Teste", "bi": "000123456LA040"}
    )

    signer = CredentialSigner()
    signed_vc = signer.sign(vc, pem)

    assert signed_vc.proof is not None
    assert "jws" in signed_vc.proof
    print(f"\n✅ Prova Criptográfica Gerada: {signed_vc.proof['jws'][:20]}...")

