from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.operadora_repository_port import OperadoraRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.outorga_espectro_repository_port import OutorgaEspectroRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusOutorga, TipoOutorga
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.outorga_espectro import OutorgaEspectro

class OutorgaEspectroService:

    def __init__(self, *, outorga_repo: OutorgaEspectroRepositoryPort, operadora_repo: OperadoraRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.outorga_repo = outorga_repo
        self.operadora_repo = operadora_repo
        self.request_service = request_service

    async def emitir_outorga(self, *, operadora_id: UUID, tipo_outorga: TipoOutorga, faixa_inicio_mhz: float, faixa_fim_mhz: float, data_outorga: date, data_validade: date | None=None, observacoes: str | None=None) -> OutorgaEspectro:
        operadora = await self.operadora_repo.get_by_id(operadora_id)
        if operadora is None:
            raise ValueError('Operadora nao encontrada para emissao da outorga')
        numero = await self.outorga_repo.next_numero()
        outorga = OutorgaEspectro.emitir(numero_outorga=numero, operadora_id=operadora_id, tipo_outorga=tipo_outorga, faixa_inicio_mhz=faixa_inicio_mhz, faixa_fim_mhz=faixa_fim_mhz, data_outorga=data_outorga, data_validade=data_validade, observacoes=observacoes)
        saved = await self.outorga_repo.save(outorga)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='EMISSAO_OUTORGA_ESPECTRO_TELECOM', entity_id=saved.id, numero_processo=saved.numero_outorga, metadata={'numero_outorga': saved.numero_outorga, 'operadora_id': str(saved.operadora_id), 'tipo_outorga': saved.tipo_outorga.value})
        return saved

    async def buscar_outorga(self, outorga_id: UUID) -> OutorgaEspectro:
        outorga = await self.outorga_repo.get_by_id(outorga_id)
        if outorga is None:
            raise ValueError('Outorga nao encontrada')
        return outorga

    async def listar_outorgas(self, *, operadora_id: UUID | None=None, status: StatusOutorga | None=None) -> list[OutorgaEspectro]:
        if operadora_id is not None:
            return await self.outorga_repo.list_by_operadora(operadora_id)
        if status is not None:
            return await self.outorga_repo.list_by_status(status)
        return await self.outorga_repo.list_all()

    async def atualizar_status(self, *, outorga_id: UUID, status: StatusOutorga) -> OutorgaEspectro:
        outorga = await self.buscar_outorga(outorga_id)
        outorga.atualizar_status(status)
        return await self.outorga_repo.save(outorga)

    async def remover_outorga(self, outorga_id: UUID) -> None:
        deleted = await self.outorga_repo.delete(outorga_id)
        if not deleted:
            raise ValueError('Outorga nao encontrada')