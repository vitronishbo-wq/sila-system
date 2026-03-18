"""
SILA 3.0: Unified Identity Service Port (Education Module)
Rule 5: No Coupling - Abstract Port for DID-based Authentication
Status: Production-ready for Dependency Injection

This port is IDENTICAL to the Health module version,
ensuring unified citizen identity verification across domains.

Pattern: Hexagonal Architecture
- Domain layer: Abstract port interface
- Application layer: Services use port
- Infrastructure layer: Concrete adapters (injected by factory)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CitizenIdentity:
    """
    DTO: Citizen identity information
    
    Rule 5: This DTO exposes ONLY what is needed for authorization.
    Internal fields (passwords, SSN, medical history) are NEVER exposed.
    
    Example of what is HIDDEN:
    - citizen_password_hash
    - medical_history
    - social_security_number
    - bank_account_data
    - employment_history
    - criminal_record
    """
    did: str
    citizen_id: str
    verified_at: datetime
    trust_score: float
    is_active: bool
    verification_method: str

@dataclass
class VerificationResult:
    """DTO: Result of identity verification"""
    is_valid: bool
    citizen: Optional[CitizenIdentity] = None
    error_message: Optional[str] = None

@dataclass
class SignatureVerificationResult:
    """DTO: Result of cryptographic signature verification"""
    is_valid: bool
    signer_did: str
    signed_at: datetime
    algorithm: str

class IdentityServicePort(ABC):
    """
    Abstract port for identity verification services.
    
    Rule 5: This port is ABSTRACT and used by Health, Education, and
    Orchestrator to verify citizen identity via DID without exposing
    internal schemas or cross-module coupling.
    
    Implementation:
    - Health module: app/modules/health/infrastructure/adapters/identity_adapter.py
    - Education module: app/modules/educacao/infrastructure/adapters/identity_adapter.py
    - Orchestrator: orchestrator/infrastructure/adapters/identity_adapter.py
    
    All implementations are IDENTICAL (same concrete adapter injected).
    """

    @abstractmethod
    async def verify_citizen_by_did(self, did: str) -> VerificationResult:
        """
        Verify a citizen's identity using their DID.
        
        Args:
            did: Decentralized Identifier (did:example:123456)
        
        Returns:
            VerificationResult with CitizenIdentity if valid
        
        Raises:
            DIDVerificationError: If DID is invalid or verification fails
        
        Example Usage (Education):
            identity_port = IdentityAdapter()  # Injected
            result = await identity_port.verify_citizen_by_did("did:sila:student123")
            if result.is_valid:
                student = result.citizen  # Only safe fields exposed
                enrollment = Enrollment(citizen_id=student.citizen_id, ...)
        
        Rule 5 Compliance:
        - Only CitizenIdentity DTO is returned (no internal schema)
        - No password, SSN, or medical data exposed
        - No direct database access from caller
        """
        pass

    @abstractmethod
    async def verify_citizen_signature(self, did: str, message: str, signature: str) -> SignatureVerificationResult:
        """
        Verify that a message was signed by a citizen with given DID.
        
        Args:
            did: Decentralized Identifier of signer
            message: Original message that was signed
            signature: Cryptographic signature (hex-encoded)
        
        Returns:
            SignatureVerificationResult indicating validity
        
        Raises:
            SignatureVerificationError: If signature verification fails
        
        Example Usage (Education):
            result = await identity_port.verify_citizen_signature(
                did="did:sila:student123",
                message="I request enrollment in course XYZ",
                signature="0x..."
            )
            if result.is_valid:
                print(f"Signed by {result.signer_did}")
        
        Rule 5 Compliance:
        - Signatures are cryptographic proofs, not credentials
        - No sensitive data is passed as message
        - Signature algorithm is transparent
        """
        pass

    @abstractmethod
    async def get_trust_score(self, did: str) -> float:
        """
        Get the trust score for a citizen.
        
        Trust score is based on:
        - Identity verification level
        - Audit trail cleanliness
        - Account age and activity history
        - Multi-factor authentication status
        
        Args:
            did: Decentralized Identifier
        
        Returns:
            Trust score (0.0 = untrusted, 1.0 = fully trusted)
        
        Example Usage (Orchestrator):
            trust = await identity_port.get_trust_score("did:sila:citizen123")
            if trust < 0.5:
                return {"status": "DENIED", "reason": "Low trust score"}
        
        Rule 5 Compliance:
        - Only numeric score returned (no internal calculation details)
        - Trust factors are not exposed
        """
        pass

    @abstractmethod
    async def validate_credential_issued_by(self, did: str, issuer_did: str) -> bool:
        """
        Validate that a citizen holds a credential issued by a specific issuer.
        
        Args:
            did: DID of credential holder
            issuer_did: DID of credential issuer (e.g., Ministry of Education)
        
        Returns:
            True if citizen holds valid credential from issuer
        
        Example Usage (Education):
            is_teacher = await identity_port.validate_credential_issued_by(
                did="did:sila:teacher123",
                issuer_did="did:sila:ministry_education"
            )
            if is_teacher:
                # Allow teacher to access student records
        
        Rule 5 Compliance:
        - Only boolean returned (no credential details exposed)
        - No schema information about credentials
        """
        pass

    @abstractmethod
    async def revoke_certificate(self, certificate_id: str, reason: str) -> bool:
        """
        Revoke a citizen certificate (revocation list update).
        
        Args:
            certificate_id: ID of certificate to revoke
            reason: Reason for revocation
        
        Returns:
            True if revocation was successful
        
        Example Usage (Orchestrator - Admin):
            success = await identity_port.revoke_certificate(
                certificate_id="cert_xyz",
                reason="EXPIRED"
            )
        
        Rule 5 Compliance:
        - Only operation status returned
        - No detailed certificate information exposed
        """
        pass

class IdentityServiceError(Exception):
    """Base exception for identity service errors"""
    pass

class DIDVerificationError(IdentityServiceError):
    """Raised when DID verification fails"""
    pass

class SignatureVerificationError(IdentityServiceError):
    """Raised when signature verification fails"""
    pass

class TrustScoreError(IdentityServiceError):
    """Raised when trust score cannot be calculated"""
    pass

class CredentialValidationError(IdentityServiceError):
    """Raised when credential validation fails"""
    pass