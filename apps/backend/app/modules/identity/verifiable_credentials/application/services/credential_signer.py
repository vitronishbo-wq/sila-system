import json
import base64
from datetime import datetime
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from app.modules.identity.verifiable_credentials.domain.entities.credential import VerifiableCredential

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
