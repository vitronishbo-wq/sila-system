"""
SILA X-Road Service: Routing, validation, and security orchestration.

Core responsibilities:
1. Trust score validation (sender must pass Trust Engine threshold)
2. Policy enforcement (sender→receiver→service_type allowed?)
3. Replay attack prevention (message_id deduplication)
4. Signature verification (PKI validation)
5. Audit trail insertion (immutable record before processing)
6. Response correlation (links request ↔ response)
"""

import hashlib
from typing import Dict, List, Optional
from datetime import datetime
import json

from app.platform.observability.logger import get_sila_logger
from app.modules.xroad.domain.envelope import (
    SILAEnvelope,
    SILAEnvelopeResponse,
    MessageStatus,
    InteroperabilityPolicy,
    OriginMinistry,
    ServiceType,
)

logger = get_sila_logger('xroad-interconnect')


class XRoadInterconnect:
    """
    SILA X-Road Security Server implementation.
    
    Coordinates atomic, signed, auditable exchanges between
    government entities (Justice, Health, Finance, etc).
    """

    def __init__(self):
        """Initialize X-Road service with policy registry."""
        self.seen_message_ids: set[str] = set()  # Replay attack prevention (in production: Redis)
        self.policies = self._init_policies()
        logger.info('✓ X-Road Interconnect initialized')

    def _init_policies(self) -> Dict[tuple, InteroperabilityPolicy]:
        """
        Define interoperability policies: who can talk to whom, about what.
        
        Returns:
            Dict[(sender, receiver)] -> InteroperabilityPolicy
        """
        policies = {}

        # Justice → Health (Birth/Death verification)
        policies[(OriginMinistry.MINJUS, OriginMinistry.MINSA)] = InteroperabilityPolicy(
            sender=OriginMinistry.MINJUS,
            receiver=OriginMinistry.MINSA,
            allowed_service_types=[
                ServiceType.VERIFY_BIRTH_NOTICE,
                ServiceType.CHECK_RESIDENCE,
                ServiceType.VALIDATE_IDENTITY,
            ],
            requires_high_trust_score=True,
            max_retry_attempts=3,
            timeout_seconds=30,
            requires_signature=True,
        )

        # Health → Justice (BI status, citizenship verification)
        policies[(OriginMinistry.MINSA, OriginMinistry.MINJUS)] = InteroperabilityPolicy(
            sender=OriginMinistry.MINSA,
            receiver=OriginMinistry.MINJUS,
            allowed_service_types=[
                ServiceType.NOTIFY_DEATH_STATUS,
                ServiceType.FETCH_BI_STATUS,
                ServiceType.VERIFY_CITIZENSHIP,
            ],
            requires_high_trust_score=True,
            max_retry_attempts=3,
            timeout_seconds=30,
            requires_signature=True,
        )

        # Bidirectional: Biometric sync
        for sender in [OriginMinistry.MINJUS, OriginMinistry.MINSA]:
            for receiver in [OriginMinistry.MINJUS, OriginMinistry.MINSA]:
                if sender != receiver:
                    key = (sender, receiver)
                    if key not in policies:
                        policies[key] = InteroperabilityPolicy(
                            sender=sender,
                            receiver=receiver,
                            allowed_service_types=[ServiceType.SYNC_BIOMETRIC],
                            requires_high_trust_score=False,
                            max_retry_attempts=5,
                            timeout_seconds=60,
                            requires_signature=True,
                        )

        logger.info(f'✓ Loaded {len(policies)} interoperability policies')
        return policies

    async def validate_envelope(self, envelope: SILAEnvelope) -> tuple[bool, str]:
        """
        Pre-flight validation before processing.
        
        Args:
            envelope: Request envelope
            
        Returns:
            (is_valid, reason)
        """

        # 1. Replay attack prevention: Have we seen this message_id?
        if envelope.message_id in self.seen_message_ids:
            logger.warning(f'⚠️ REPLAY DETECTED: message_id={envelope.message_id}')
            return False, f'Message ID already processed (replay attack prevented)'

        # 2. Trust score threshold check
        if envelope.trust_score is None or envelope.trust_score < 0.80:
            logger.warning(
                f'⚠️ LOW TRUST: sender={envelope.sender_service} '
                f'score={envelope.trust_score} (required: >= 0.80)'
            )
            return False, f'Sender trust score {envelope.trust_score} below threshold (0.80)'

        # 3. Policy enforcement: Is this combination allowed?
        policy_key = (envelope.sender_service, envelope.receiver_service)
        policy = self.policies.get(policy_key)

        if not policy:
            logger.warning(
                f'⚠️ POLICY VIOLATION: {envelope.sender_service} '
                f'→ {envelope.receiver_service} (no policy defined)'
            )
            return False, f'No interoperability policy for {policy_key}'

        if envelope.service_type not in policy.allowed_service_types:
            logger.warning(
                f'⚠️ SERVICE FORBIDDEN: {envelope.sender_service} '
                f'cannot invoke {envelope.service_type} on {envelope.receiver_service}'
            )
            return False, (
                f'Service {envelope.service_type} not allowed for '
                f'{policy_key[0]} → {policy_key[1]}'
            )

        if (
            policy.requires_high_trust_score
            and envelope.trust_score < 0.85
        ):
            logger.warning(
                f'⚠️ HIGH TRUST REQUIRED: {envelope.sender_service} '
                f'score={envelope.trust_score} needs >= 0.85'
            )
            return False, f'High trust score required (got {envelope.trust_score}, need 0.85)'

        # 4. Signature validation (placeholder - real implementation validates PKI)
        if policy.requires_signature and not envelope.signature:
            logger.warning(f'⚠️ SIGNATURE MISSING: message_id={envelope.message_id}')
            return False, f'Signature required but not provided'

        logger.info(
            f'✓ Envelope validated: {envelope.sender_service} '
            f'→ {envelope.receiver_service} ({envelope.service_type})'
        )
        return True, ''

    async def exchange(self, envelope: SILAEnvelope) -> SILAEnvelopeResponse:
        """
        Process X-Road exchange: Route request to receiver, return response.
        
        Args:
            envelope: Inbound SILA envelope
            
        Returns:
            SILAEnvelopeResponse with correlation_id linking to request
        """

        envelope_str = json.dumps(envelope.model_dump(exclude={'signature'}))
        audit_id = hashlib.sha256(envelope_str.encode()).hexdigest()[:16]

        try:
            # Step 1: Validate
            is_valid, reason = await self.validate_envelope(envelope)
            if not is_valid:
                logger.error(f'✗ Validation failed: {reason}')
                return SILAEnvelopeResponse(
                    correlation_id=envelope.message_id,
                    status=MessageStatus.REPLAY_BLOCKED
                    if 'replay' in reason.lower()
                    else MessageStatus.CREATED,
                    timestamp=datetime.utcnow().isoformat(),
                    payload={'error': reason},
                    error=reason,
                    audit_record_id=audit_id,
                )

            # Step 2: Mark as seen (prevent replays)
            self.seen_message_ids.add(envelope.message_id)

            # Step 3: Insert into audit trail BEFORE processing
            await self._audit_insert(envelope, audit_id, 'RECEIVED')
            logger.info(f'✓ Audit recorded: {audit_id}')

            # Step 4: Route to handler (stub - real implementation dispatches)
            result = await self._route_service(envelope)

            # Step 5: Insert response into audit trail
            await self._audit_insert(envelope, audit_id, 'PROCESSED', result)

            logger.info(
                f'✓ Exchange complete: '
                f'{envelope.sender_service} → {envelope.receiver_service} '
                f'({envelope.service_type})'
            )

            return SILAEnvelopeResponse(
                correlation_id=envelope.message_id,
                status=MessageStatus.PROCESSED,
                timestamp=datetime.utcnow().isoformat(),
                payload=result,
                audit_record_id=audit_id,
            )

        except Exception as e:
            logger.error(f'✗ Exchange failed: {str(e)}')
            return SILAEnvelopeResponse(
                correlation_id=envelope.message_id,
                status=MessageStatus.CREATED,
                timestamp=datetime.utcnow().isoformat(),
                payload={},
                error=str(e),
                audit_record_id=audit_id,
            )

    async def _route_service(self, envelope: SILAEnvelope) -> Dict:
        """
        Route to service handler based on service_type.
        
        Args:
            envelope: Validated envelope
            
        Returns:
            Service-specific response payload
        """

        # In production, these would call actual service implementations
        service_handlers = {
            ServiceType.VERIFY_BIRTH_NOTICE: self._handle_verify_birth,
            ServiceType.NOTIFY_DEATH_STATUS: self._handle_notify_death,
            ServiceType.VALIDATE_IDENTITY: self._handle_validate_identity,
            ServiceType.CHECK_RESIDENCE: self._handle_check_residence,
            ServiceType.FETCH_BI_STATUS: self._handle_fetch_bi,
            ServiceType.VERIFY_CITIZENSHIP: self._handle_verify_citizenship,
            ServiceType.SYNC_BIOMETRIC: self._handle_sync_biometric,
            ServiceType.HEALTH_CHECK: self._handle_health_check,
        }

        handler = service_handlers.get(envelope.service_type)
        if not handler:
            logger.warning(f'⚠️ No handler for {envelope.service_type}')
            return {'error': f'Service not implemented: {envelope.service_type}'}

        return await handler(envelope)

    # Service handlers (stubs - real implementations contact actual services)
    async def _handle_verify_birth(self, envelope: SILAEnvelope) -> Dict:
        return {'verified': True, 'source': 'MINSA_MATERNIDADE', 'record_id': 'NASCIMENTO_123'}

    async def _handle_notify_death(self, envelope: SILAEnvelope) -> Dict:
        return {'status': 'record_updated', 'entity': 'Conservatória', 'bi_status': 'INVALID'}

    async def _handle_validate_identity(self, envelope: SILAEnvelope) -> Dict:
        return {'valid': True, 'name': 'Cidadão Exemplo', 'citizen_id': '123456789'}

    async def _handle_check_residence(self, envelope: SILAEnvelope) -> Dict:
        return {'resident': True, 'address': 'Luanda, Angola', 'verified_at': datetime.utcnow().isoformat()}

    async def _handle_fetch_bi(self, envelope: SILAEnvelope) -> Dict:
        return {'bi_status': 'ACTIVE', 'issue_date': '2020-01-01', 'expiry_date': '2030-01-01'}

    async def _handle_verify_citizenship(self, envelope: SILAEnvelope) -> Dict:
        return {'citizen': True, 'country': 'ANGOLA', 'confirmed': True}

    async def _handle_sync_biometric(self, envelope: SILAEnvelope) -> Dict:
        return {'synced': True, 'fingerprints': 10, 'face_template': 'updated'}

    async def _handle_health_check(self, envelope: SILAEnvelope) -> Dict:
        return {'status': 'online', 'timestamp': datetime.utcnow().isoformat()}

    async def _audit_insert(self, envelope: SILAEnvelope, audit_id: str, status: str, result: Dict = None) -> None:
        """
        Insert audit trail record (immutable log).
        
        In production: Append to blockchain or WORM storage.
        For now: Log to observability system.
        """
        audit_entry = {
            'audit_id': audit_id,
            'message_id': envelope.message_id,
            'sender': envelope.sender_service.value,
            'receiver': envelope.receiver_service.value,
            'service_type': envelope.service_type.value,
            'status': status,
            'timestamp': datetime.utcnow().isoformat(),
            'trust_score': envelope.trust_score,
            'result': result,
        }

        logger.info(f'📋 AUDIT: {json.dumps(audit_entry)}')

    async def list_services(self) -> Dict:
        """List all available X-Road services."""
        return {
            'available_services': [h.value for h in ServiceType],
            'total': len(ServiceType),
            'interop_policy_count': len(self.policies),
        }
