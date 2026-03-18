#!/bin/bash
set -e

BASE_PATH="app/modules/identity/subdomains/verifiable_credentials"
TEST_PATH="app/modules/identity/tests"

echo "🚀 [SILA-AUTH] Hidratando Verifiable Credentials Engine..."

# 1. Estrutura de Domínio
cat << 'INNER_EOF' > $BASE_PATH/domain/entities/credential.py
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class VerifiableCredential(BaseModel):
    context: List[str] = Field(default=["https://www.w3.org/2018/credentials/v1"], alias="@context")
    id: str
    type: List[str] = ["VerifiableCredential"]
    issuer: str
    issuance_date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    credential_subject: Dict[str, Any]
    proof: Optional[Dict[str, Any]] = None

    class Config:
        populate_by_name = True
INNER_EOF

# 2. Motor de Assinatura (Signer)
cat << 'INNER_EOF' > $BASE_PATH/application/services/credential_signer.py
import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from app.modules.identity.subdomains.verifiable_credentials.domain.entities.credential import VerifiableCredential

class CredentialSigner:
    def sign(self, vc: VerifiableCredential, private_key_pem: bytes) -> VerifiableCredential:
        vc_dict = vc.model_dump(by_alias=True, exclude={'proof'})
        payload = json.dumps(vc_dict, sort_keys=True).encode('utf-8')
        
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
        
        signature = private_key.sign(
            payload,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        
        vc.proof = {
            "type": "RsaSignature2018",
            "created": datetime.utcnow().isoformat(),
            "proofPurpose": "assertionMethod",
            "verificationMethod": f"{vc.issuer}#key-1",
            "jws": base64.b64encode(signature).decode('utf-8')
        }
        return vc
INNER_EOF

# 3. Teste Unitário (Aumento de Cobertura)
mkdir -p $TEST_PATH
cat << 'INNER_EOF' > $TEST_PATH/test_vc_issuance.py
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from app.modules.identity.subdomains.verifiable_credentials.domain.entities.credential import VerifiableCredential
from app.modules.identity.subdomains.verifiable_credentials.application.services.credential_signer import CredentialSigner

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

INNER_EOF

echo "✅ [SILA-AUTH] Módulo hidratado. Rodando auditoria..."
