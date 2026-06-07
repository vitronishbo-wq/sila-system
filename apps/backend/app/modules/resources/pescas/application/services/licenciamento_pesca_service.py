from __future__ import annotations

from datetime import date, timedelta
from uuid import UUID

from apps.backend.app.modules.resources.pescas.application.ports import (
    EmbarcacaoRepositoryPort,
    LicencaPescaRepositoryPort,
)
from apps.backend.app.modules.resources.pescas.domain.models.licenca_pesca import LicencaPesca


class LicenciamentoPescaService:
    def __init__(
        self, licenca_repo: LicencaPescaRepositoryPort, embarcacao_repo: EmbarcacaoRepositoryPort
    ):
        self.licenca_repo = licenca_repo
        self.embarcacao_repo = embarcacao_repo

    async def emitir_licenca(
        self,
        *,
        embarcacao_id: UUID,
        titular_id: UUID,
        modalidade_autorizada: str,
        zona_pesca_id: UUID,
        validade_dias: int = 365,
    ) -> LicencaPesca:
        embarcacao = await self.embarcacao_repo.get_by_id(embarcacao_id)
        if not embarcacao:
            raise ValueError("Embarcacao nao encontrada")
        numero_licenca = await self.licenca_repo.next_numero()
        hoje = date.today()
        item = LicencaPesca.emitir(
            numero_licenca=numero_licenca,
            embarcacao_id=embarcacao_id,
            titular_id=titular_id,
            data_emissao=hoje,
            data_validade=hoje + timedelta(days=validade_dias),
            modalidade_autorizada=modalidade_autorizada,
            zona_pesca_id=zona_pesca_id,
        )
        return await self.licenca_repo.save(item)

    async def buscar_licenca(self, licenca_id: UUID) -> LicencaPesca:
        item = await self.licenca_repo.get_by_id(licenca_id)
        if not item:
            raise ValueError("Licenca nao encontrada")
        return item

    async def listar_licencas_validas(self) -> list[LicencaPesca]:
        return await self.licenca_repo.list_validas(date.today())
