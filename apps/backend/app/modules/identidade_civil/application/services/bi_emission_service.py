from app.core.observability import trace
from typing import Dict, Any, Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.identidade_civil.infrastructure.repositories.bi_repository import BIRepository
from app.modules.identidade_civil.infrastructure.repositories.identity_request_repository import IdentityRequestRepository
from app.modules.identidade_civil.exceptions import BusinessRuleException, SovereigntyValidationException


class BIEmissionService:
    """Lightweight BI emission service used by tests.

    This implementation is intentionally minimal: it validates citizen
    existence/eligibility via the provided FUC client, checks for an
    existing active BI, and persists an IdentityRequest record.
    """
    def __init__(self, session: AsyncSession, fuc_client):
        self.session = session
        self.fuc_client = fuc_client
        self.bi_repo = BIRepository(session)
        self.ir_repo = IdentityRequestRepository(session)

    @trace()
    async def execute_emission(self, citizen_fuc_id: str, operator_id: str, notes: Optional[str] = None) -> Dict[str, Any]:
        # 1. Verify citizen exists
        projection = await self.fuc_client.get_citizen_by_id(citizen_fuc_id)
        if projection is None:
            raise SovereigntyValidationException(detail=f"Cidadão {citizen_fuc_id} não encontrado")

        # 2. Check eligibility
        eligible = await self.fuc_client.validate_eligibility(citizen_fuc_id, "001")
        if not eligible:
            raise BusinessRuleException(detail=f"Cidadão {citizen_fuc_id} não é elegível")

        # 3. Check existing active BI
        existing_bi = await self.bi_repo.get_active_by_citizen(citizen_fuc_id)
        if existing_bi:
            raise BusinessRuleException(detail=f"BI ativo encontrado: {existing_bi.bi_number}")

        # 4. Persist IdentityRequest
        req_id = uuid.uuid4()
        payload = {
            "citizen_snapshot": {
                "full_name": getattr(projection, "full_name", None)
            },
            "notes": ["created by BIEmissionService", notes] if notes else ["created by BIEmissionService"]
        }

        request_obj = {
            "id": req_id,
            "citizen_fuc_id": citizen_fuc_id,
            "service_code": "001",
            "status": "approved",
            "payload": payload,
        }

        saved = await self.ir_repo.save(request_obj)

        return {
            "success": True,
            "request_id": str(saved.id),
            "status": "approved",
            "citizen_name": payload["citizen_snapshot"]["full_name"],
        }
