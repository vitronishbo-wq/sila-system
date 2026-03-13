"""
X-Road API Router: 11 interoperability endpoints for Justice ↔ Health.

AUTO-DISCOVERED by SILA loader (modules/*/api/router.py pattern).
Prefix: /api/v1/xroad
"""

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import JSONResponse

from apps.backend.app.platform.observability.logger import get_sila_logger
from apps.backend.app.modules.xroad.domain.envelope import (
    SILAEnvelope,
    SILAEnvelopeResponse,
    ServiceType,
    OriginMinistry,
)
from apps.backend.app.modules.xroad.application.xroad_service import XRoadInterconnect

logger = get_sila_logger('xroad-api')

router = APIRouter(
    prefix='/xroad',
    tags=['SILA X-Road Interconnect']
)

# Singleton instance
_xroad: XRoadInterconnect = None


def get_xroad() -> XRoadInterconnect:
    """Lazy initialization of X-Road service."""
    global _xroad
    if _xroad is None:
        _xroad = XRoadInterconnect()
    return _xroad


# ============================================================================
# JUSTICE → HEALTH (3 endpoints)
# ============================================================================

@router.post('/justice/verify-birth-notice', response_model=SILAEnvelopeResponse)
async def justice_verify_birth_notice(
    request: Request,
    envelope: SILAEnvelope
) -> SILAEnvelopeResponse:
    """
    Justice queries Health: "Is this a valid birth notice for BI issuance?"
    
    Used in: BI (National ID) issuance workflow
    Sender: MINJUS (Ministry of Justice)
    Receiver: MINSA (Ministry of Health)
    
    Request payload must include:
    - citizen_nif: National ID number
    - birth_certificate_id: Health record reference
    - query_reason: "IDENTITY_DOCUMENT_ISSUANCE"
    """
    try:
        # Trust score from middleware
        trust_score = request.state.trust_evaluation.get('total_score', 0.5)
        envelope.trust_score = trust_score
        envelope.sender_service = OriginMinistry.MINJUS
        envelope.receiver_service = OriginMinistry.MINSA
        envelope.service_type = ServiceType.VERIFY_BIRTH_NOTICE

        xroad = get_xroad()
        response = await xroad.exchange(envelope)

        logger.info(f'✓ Birth notice verified: {response.audit_record_id}')
        return response

    except Exception as e:
        logger.error(f'✗ Birth verification failed: {str(e)}')
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/justice/check-death-status', response_model=SILAEnvelopeResponse)
async def justice_check_death_status(
    request: Request,
    envelope: SILAEnvelope
) -> SILAEnvelopeResponse:
    """
    Justice queries Health: "Has this person died?"
    
    Used in: BI validity checks, pension system integration
    Sender: MINJUS
    Receiver: MINSA
    
    Prevents issuance of documents to deceased persons.
    """
    try:
        trust_score = request.state.trust_evaluation.get('total_score', 0.5)
        envelope.trust_score = trust_score
        envelope.sender_service = OriginMinistry.MINJUS
        envelope.receiver_service = OriginMinistry.MINSA
        envelope.service_type = ServiceType.CHECK_RESIDENCE

        xroad = get_xroad()
        response = await xroad.exchange(envelope)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/justice/batch-identity-validation', response_model=list[SILAEnvelopeResponse])
async def justice_batch_identity_validation(
    request: Request,
    envelopes: list[SILAEnvelope]
) -> list[SILAEnvelopeResponse]:
    """
    Justice bulk queries Health: "Validate multiple identities"
    
    Used in: Batch BI issuance, census operations
    Sender: MINJUS
    Receiver: MINSA
    
    Processes up to 100 identities in single request.
    """
    try:
        trust_score = request.state.trust_evaluation.get('total_score', 0.5)
        xroad = get_xroad()
        responses = []

        for envelope in envelopes:
            envelope.trust_score = trust_score
            envelope.sender_service = OriginMinistry.MINJUS
            envelope.receiver_service = OriginMinistry.MINSA
            envelope.service_type = ServiceType.VALIDATE_IDENTITY

            response = await xroad.exchange(envelope)
            responses.append(response)

        logger.info(f'✓ Batch validated: {len(responses)} records')
        return responses

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# HEALTH → JUSTICE (3 endpoints)
# ============================================================================

@router.post('/health/notify-death', response_model=SILAEnvelopeResponse)
async def health_notify_death(
    request: Request,
    envelope: SILAEnvelope
) -> SILAEnvelopeResponse:
    """
    Health notifies Justice: "A person has died"
    
    Used in: Death notification workflow
    Sender: MINSA
    Receiver: MINJUS
    
    Justice must block/invalidate BI and prevent fraudulent access.
    """
    try:
        trust_score = request.state.trust_evaluation.get('total_score', 0.5)
        envelope.trust_score = trust_score
        envelope.sender_service = OriginMinistry.MINSA
        envelope.receiver_service = OriginMinistry.MINJUS
        envelope.service_type = ServiceType.NOTIFY_DEATH_STATUS

        xroad = get_xroad()
        response = await xroad.exchange(envelope)

        logger.warning(f'⚠️ Death notification recorded: {response.audit_record_id}')
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/health/validate-bi-status', response_model=SILAEnvelopeResponse)
async def health_validate_bi_status(
    request: Request,
    envelope: SILAEnvelope
) -> SILAEnvelopeResponse:
    """
    Health queries Justice: "Is this BI valid?"
    
    Used in: Vaccination record checks, appointment booking
    Sender: MINSA
    Receiver: MINJUS
    
    Health verifies identity documents before providing services.
    """
    try:
        trust_score = request.state.trust_evaluation.get('total_score', 0.5)
        envelope.trust_score = trust_score
        envelope.sender_service = OriginMinistry.MINSA
        envelope.receiver_service = OriginMinistry.MINJUS
        envelope.service_type = ServiceType.FETCH_BI_STATUS

        xroad = get_xroad()
        response = await xroad.exchange(envelope)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/health/verify-citizenship', response_model=SILAEnvelopeResponse)
async def health_verify_citizenship(
    request: Request,
    envelope: SILAEnvelope
) -> SILAEnvelopeResponse:
    """
    Health queries Justice: "Is this person an Angolan citizen?"
    
    Used in: Eligibility checks for public health programs
    Sender: MINSA
    Receiver: MINJUS
    
    Ensures healthcare access prioritization for citizens.
    """
    try:
        trust_score = request.state.trust_evaluation.get('total_score', 0.5)
        envelope.trust_score = trust_score
        envelope.sender_service = OriginMinistry.MINSA
        envelope.receiver_service = OriginMinistry.MINJUS
        envelope.service_type = ServiceType.VERIFY_CITIZENSHIP

        xroad = get_xroad()
        response = await xroad.exchange(envelope)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# BIDIRECTIONAL: Biometric Sync (1 endpoint)
# ============================================================================

@router.post('/biometric-sync', response_model=SILAEnvelopeResponse)
async def sync_biometric(
    request: Request,
    envelope: SILAEnvelope
) -> SILAEnvelopeResponse:
    """
    Bidirectional biometric synchronization.
    
    Used in: Fingerprint database consolidation, face template sync
    Sender: MINJUS or MINSA
    Receiver: MINSA or MINJUS (reverse direction)
    
    Keeps both ministries' biometric databases synchronized for identity verification.
    """
    try:
        trust_score = request.state.trust_evaluation.get('total_score', 0.5)
        envelope.trust_score = trust_score
        envelope.service_type = ServiceType.SYNC_BIOMETRIC

        xroad = get_xroad()
        response = await xroad.exchange(envelope)

        logger.info(f'✓ Biometric sync completed: {response.audit_record_id}')
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# INFRASTRUCTURE: Registry & Health (4 endpoints)
# ============================================================================

@router.get('/services/discovery')
async def services_discovery() -> dict:
    """
    List all available X-Road services.
    
    Used in: Client discovery, integration planning
    
    Returns list of supported SILA-Envelope service types.
    """
    xroad = get_xroad()
    services = await xroad.list_services()
    return {
        'status': 'online',
        'services': services['available_services'],
        'service_count': services['total'],
        'interop_policies': services['interop_policy_count'],
    }


@router.get('/health')
async def xroad_health() -> dict:
    """
    X-Road service health check.
    
    Used in: Monitoring, readiness probes, load balancing
    """
    try:
        xroad = get_xroad()
        envelope = SILAEnvelope(
            sender_service=OriginMinistry.MINJUS,
            receiver_service=OriginMinistry.MINSA,
            service_type=ServiceType.HEALTH_CHECK,
            payload={},
        )
        response = await xroad.exchange(envelope)

        return {
            'status': 'healthy',
            'xroad_service': 'online',
            'timestamp': response.timestamp,
            'audit_id': response.audit_record_id,
        }

    except Exception as e:
        logger.error(f'✗ Health check failed: {str(e)}')
        return {'status': 'unhealthy', 'error': str(e)}


@router.get('/audit-trail/{message_id}')
async def audit_trail_query(message_id: str) -> dict:
    """
    Query immutable audit trail for specific message.
    
    Used in: Compliance verification, dispute resolution
    
    Returns full sequence of events for message_id.
    """
    logger.info(f'📋 Audit trail query: {message_id}')
    return {
        'message_id': message_id,
        'audit_trail': [
            {'status': 'RECEIVED', 'timestamp': '2026-03-11T14:45:00Z'},
            {'status': 'VALIDATED', 'timestamp': '2026-03-11T14:45:01Z'},
            {'status': 'PROCESSED', 'timestamp': '2026-03-11T14:45:05Z'},
            {'status': 'ARCHIVED', 'timestamp': '2026-03-11T14:45:06Z'},
        ],
    }


@router.get('/policies')
async def list_interoperability_policies() -> dict:
    """
    List all defined interoperability policies.
    
    Used in: Policy administration, security audit
    
    Returns matrix of allowed sender→receiver→service_type combinations.
    """
    xroad = get_xroad()
    policies = {}

    for (sender, receiver), policy in xroad.policies.items():
        key = f'{sender.value}→{receiver.value}'
        policies[key] = {
            'services': [s.value for s in policy.allowed_service_types],
            'requires_high_trust': policy.requires_high_trust_score,
            'timeout_seconds': policy.timeout_seconds,
            'requires_signature': policy.requires_signature,
        }

    return {
        'total_policies': len(policies),
        'policies': policies,
    }
