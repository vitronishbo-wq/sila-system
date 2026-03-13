from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.operadora_repository_port import OperadoraRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.sla_repository_port import SLARepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusSLA, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.sla import SLA

class SLAService:

    def __init__(self, *, sla_repo: SLARepositoryPort, operadora_repo: OperadoraRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.sla_repo = sla_repo
        self.operadora_repo = operadora_repo
        self.request_service = request_service

    async def criar_sla(self, *, operadora_id: UUID, nome: str, servico: TipoServico, disponibilidade_min_percentual: float, latencia_max_ms: float, jitter_max_ms: float, perda_pacotes_max_percentual: float, velocidade_download_min_mbps: float, velocidade_upload_min_mbps: float, data_inicio: date, data_fim: date | None=None, observacoes: str | None=None) -> SLA:
        operadora = await self.operadora_repo.get_by_id(operadora_id)
        if operadora is None:
            raise ValueError('Operadora nao encontrada para cadastro do SLA')
        if servico not in operadora.servicos_autorizados:
            raise ValueError('Servico informado nao esta autorizado para a operadora')
        codigo = await self.sla_repo.next_codigo()
        sla = SLA.criar(codigo_sla=codigo, operadora_id=operadora_id, nome=nome, servico=servico, disponibilidade_min_percentual=disponibilidade_min_percentual, latencia_max_ms=latencia_max_ms, jitter_max_ms=jitter_max_ms, perda_pacotes_max_percentual=perda_pacotes_max_percentual, velocidade_download_min_mbps=velocidade_download_min_mbps, velocidade_upload_min_mbps=velocidade_upload_min_mbps, data_inicio=data_inicio, data_fim=data_fim, observacoes=observacoes)
        saved = await self.sla_repo.save(sla)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_SLA_TELECOM', entity_id=saved.id, numero_processo=saved.codigo_sla, metadata={'codigo_sla': saved.codigo_sla, 'operadora_id': str(saved.operadora_id), 'servico': saved.servico.value})
        return saved

    async def buscar_sla(self, sla_id: UUID) -> SLA:
        sla = await self.sla_repo.get_by_id(sla_id)
        if sla is None:
            raise ValueError('SLA nao encontrado')
        return sla

    async def listar_slas(self, *, operadora_id: UUID | None=None, status: StatusSLA | None=None) -> list[SLA]:
        if operadora_id is not None:
            return await self.sla_repo.list_by_operadora(operadora_id)
        if status is not None:
            return await self.sla_repo.list_by_status(status)
        return await self.sla_repo.list_all()

    async def atualizar_status(self, *, sla_id: UUID, status: StatusSLA) -> SLA:
        sla = await self.buscar_sla(sla_id)
        sla.atualizar_status(status)
        return await self.sla_repo.save(sla)

    async def remover_sla(self, sla_id: UUID) -> None:
        deleted = await self.sla_repo.delete(sla_id)
        if not deleted:
            raise ValueError('SLA nao encontrado')