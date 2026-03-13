from __future__ import annotations
from uuid import UUID
from app.modules.society.assistencia_social.application.ports import SaudeServicePort

class SaudeServiceAdapter(SaudeServicePort):

    async def validar_laudo_pcd(self, *, citizen_id: UUID, laudo_id: UUID, cid: str) -> bool:
        return bool(citizen_id and laudo_id and cid.strip())

    async def verificar_cobertura_idoso(self, *, citizen_id: UUID) -> bool:
        return bool(citizen_id)