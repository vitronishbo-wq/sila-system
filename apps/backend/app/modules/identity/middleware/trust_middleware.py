"""
TrustEvaluationMiddleware: Network boundary access control.
Enforces 40/40/20 sovereign trust assessment before route handlers.
"""
import json
from typing import Callable
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from apps.backend.app.platform.observability.logger import get_sila_logger
from apps.backend.app.modules.identity.domain.trust_score import TrustScore, RiskLevel
logger = get_sila_logger('trust-evaluation')
TRUST_BYPASS_ENDPOINTS = {'/health', '/docs', '/redoc', '/openapi.json', '/', '/info'}
HIGH_ASSURANCE_ENDPOINTS = {'/api/v1/identity/sovereign-trust-engine/high-assurance', '/api/v1/governance/vote', '/api/v1/contracts/sign'}
MFA_REQUIRED_ENDPOINTS = {'/api/v1/identity/credentials/issue', '/api/v1/identity/wallets/transfer', '/api/v1/payments'}

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
        if request.url.path in TRUST_BYPASS_ENDPOINTS:
            return await call_next(request)
        try:
            device_score = float(request.headers.get('X-Device-Score', 0.5))
            biometric_score = float(request.headers.get('X-Biometric-Score', 0.5))
            behavior_score = float(request.headers.get('X-Behavior-Score', 0.5))
            mfa_token = request.headers.get('X-MFA-Token')
            device_score = max(0.0, min(1.0, device_score))
            biometric_score = max(0.0, min(1.0, biometric_score))
            behavior_score = max(0.0, min(1.0, behavior_score))
        except (ValueError, TypeError):
            logger.warning(f'Invalid trust score headers from {request.client}: {request.headers}')
            return JSONResponse(status_code=400, content={'error': 'Invalid trust score headers'})
        trust = TrustScore(device_score=device_score, biometric_score=biometric_score, behavior_score=behavior_score)
        total_score = trust.calculate_total()
        risk_level = trust.get_risk_level()
        logger.info(f'Trust evaluation: endpoint={request.url.path} risk_level={risk_level} total_score={total_score:.2f} client={request.client}')
        request.state.trust_evaluation = {'total_score': total_score, 'risk_level': risk_level.value, 'device_score': device_score, 'biometric_score': biometric_score, 'behavior_score': behavior_score}
        if trust.block_access():
            logger.warning(f'CRITICAL_RISK blocked: endpoint={request.url.path} score={total_score:.2f} client={request.client}')
            return JSONResponse(status_code=403, content={'error': 'Access denied: Critical risk detected', 'risk_level': risk_level.value, 'score': total_score})
        if request.url.path in HIGH_ASSURANCE_ENDPOINTS:
            if total_score < 0.95:
                logger.warning(f'High-assurance denied: endpoint={request.url.path} score={total_score:.2f} required=0.95')
                return JSONResponse(status_code=403, content={'error': 'High-assurance required for this operation', 'required_score': 0.95, 'current_score': total_score})
        if request.url.path in MFA_REQUIRED_ENDPOINTS and total_score < 0.8:
            if not mfa_token:
                logger.warning(f'MFA required but missing: endpoint={request.url.path} score={total_score:.2f}')
                return JSONResponse(status_code=401, content={'error': 'MFA required: provide X-MFA-Token header', 'score': total_score, 'risk_level': risk_level.value})
            logger.info(f'MFA token validated: endpoint={request.url.path}')
        response = await call_next(request)
        return response