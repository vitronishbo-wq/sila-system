from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.resources.pescas.application.ports import CapturaRepositoryPort, LicencaPescaRepositoryPort
from apps.backend.app.modules.resources.pescas.domain.enums import StatusLicenca
from apps.backend.app.modules.resources.pescas.domain.models.captura import Captura

class CapturaService:

    def __init__(self, captura_repo: CapturaRepositoryPort, licenca_repo: LicencaPescaRepositoryPort):
        self.captura_repo = captura_repo
        self.licenca_repo = licenca_repo

    async def registrar_captura(self, *, embarcacao_id: UUID, licenca_id: UUID, zona_pesca_id: UUID, especie_id: UUID, quantidade_kg: Decimal, arte_pesca_id: UUID) -> Captura:
        licenca = await self.licenca_repo.get_by_id(licenca_id)
        if not licenca:
            raise ValueError('Licenca nao encontrada')
        if licenca.status not in {StatusLicenca.DEFERIDA, StatusLicenca.EM_ANALISE}:
            raise ValueError('Licenca sem status valido para captura')
        if licenca.data_validade < date.today():
            raise ValueError('Licenca vencida')
        item = Captura.registrar(embarcacao_id=embarcacao_id, licenca_id=licenca_id, zona_pesca_id=zona_pesca_id, especie_id=especie_id, quantidade_kg=quantidade_kg, arte_pesca_id=arte_pesca_id)
        return await self.captura_repo.save(item)

    async def buscar_captura(self, captura_id: UUID) -> Captura:
        item = await self.captura_repo.get_by_id(captura_id)
        if not item:
            raise ValueError('Captura nao encontrada')
        return item

    async def listar_capturas(self, embarcacao_id: UUID) -> list[Captura]:
        return await self.captura_repo.list_by_embarcacao(embarcacao_id)