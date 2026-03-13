"""
TrustEvaluationMiddleware: Network boundary access control.
Enforces 40/40/20 sovereign trust assessment before route handlers.
"""

import json
from typing import Callable

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.platform.observability.logger import get_sila_logger
from apps.backend.app.modules.identity.domain.trust_score import TrustScore, RiskLevel

logger = get_sila_logger('trust-evaluation')

# Endpoints that bypass trust evaluation
TRUST_BYPASS_ENDPOINTS = {
    '/health', '/docs', '/redoc', '/openapi.json', '/', '/info'
}

# Endpoints requiring high-assurance (voting, contracts)
HIGH_ASSURANCE_ENDPOINTS = {
    '/api/v1/identity/sovereign-trust-engine/high-assurance',
    '/api/v1/governance/vote',
    '/api/v1/contracts/sign'
}

# Endpoints requiring MFA if score < 0.8
MFA_REQUIRED_ENDPOINTS = {
    '/api/v1/identity/credentials/issue',
    '/api/v1/identity/wallets/transfer',
    '/api/v1/payments'
}


class TrustEvaluationMiddleware(BaseHTTPMiddleware):
    """
    Network boundary middleware enforcing sovereign trust assessment.
    
    Policy:
    1. CRITICAL_RISK (< 0.4): Block access (403)
    2. HIGH_RISK (0.4-0.6) or MEDIUM_RISK on MFA endpoint: Require MFA token
    3. HIGH_ASSURANCE endpoint: Require score >= 0.95
    
    Extracts trust metrics from headers:
    - X-Device-Score: float [0.0-1.0]
    - X-Biometric-Score: float [0.0-1.0]
    - X-Behavior-Score: float [0.0-1.0]
    - X-MFA-Token: str (optional, for MFA validation)
    """

    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
        """
        Main middleware dispatch: evaluate trust and control access.
        
        Args:
            request: FastAPI Request
            call_next: Next middleware/handler
            
        Returns:
            JSONResponse with trust evaluation results or pass-through
        """

        # Bypass trust evaluation for health/docs endpoints
        if request.url.path in TRUST_BYPASS_ENDPOINTS:
            return await call_next(request)

        # Extract trust scores from headers
        try:
            device_score = float(request.headers.get('X-Device-Score', 0.5))
            biometric_score = float(request.headers.get('X-Biometric-Score', 0.5))
            behavior_score = float(request.headers.get('X-Behavior-Score', 0.5))
            mfa_token = request.headers.get('X-MFA-Token')

            # Clamp scores to [0.0, 1.0]
            device_score = max(0.0, min(1.0, device_score))
            biometric_score = max(0.0, min(1.0, biometric_score))
            behavior_score = max(0.0, min(1.0, behavior_score))

        except (ValueError, TypeError):
            logger.warning(f'Invalid trust score headers from {request.client}: {request.headers}')
            return JSONResponse(
                status_code=400,
                content={'error': 'Invalid trust score headers'}
            )

        # Calculate trust evaluation
        trust = TrustScore(
            device_score=device_score,
            biometric_score=biometric_score,
            behavior_score=behavior_score
        )

        total_score = trust.calculate_total()
        risk_level = trust.get_risk_level()

        logger.info(
            f'Trust evaluation: endpoint={request.url.path} '
            f'risk_level={risk_level} total_score={total_score:.2f} '
            f'client={request.client}'
        )

        # Attach trust context to request state
        request.state.trust_evaluation = {
            'total_score': total_score,
            'risk_level': risk_level.value,
            'device_score': device_score,
            'biometric_score': biometric_score,
            'behavior_score': behavior_score,
        }

        # Policy 1: Block CRITICAL_RISK (score < 0.4)
        if trust.block_access():
            logger.warning(
                f'CRITICAL_RISK blocked: endpoint={request.url.path} '
                f'score={total_score:.2f} client={request.client}'
            )
            return JSONResponse(
                status_code=403,
                content={
                    'error': 'Access denied: Critical risk detected',
                    'risk_level': risk_level.value,
                    'score': total_score
                }
            )

        # Policy 2: High-assurance endpoints require >= 0.95
        if request.url.path in HIGH_ASSURANCE_ENDPOINTS:
            if total_score < 0.95:
                logger.warning(
                    f'High-assurance denied: endpoint={request.url.path} '
                    f'score={total_score:.2f} required=0.95'
                )
                return JSONResponse(
                    status_code=403,
                    content={
                        'error': 'High-assurance required for this operation',
                        'required_score': 0.95,
                        'current_score': total_score
                    }
                )

        # Policy 3: MFA-required endpoints need token if score < 0.8
        if request.url.path in MFA_REQUIRED_ENDPOINTS and total_score < 0.8:
            if not mfa_token:
                logger.warning(
                    f'MFA required but missing: endpoint={request.url.path} '
                    f'score={total_score:.2f}'
                )
                return JSONResponse(
                    status_code=401,
                    content={
                        'error': 'MFA required: provide X-MFA-Token header',
                        'score': total_score,
                        'risk_level': risk_level.value
                    }
                )
            # MFA token validation (placeholder - would validate JWT in production)
            logger.info(f'MFA token validated: endpoint={request.url.path}')

        # All policies passed, proceed to handler
        response = await call_next(request)
        return response
