from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.assinante_repository_port import AssinanteRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.operadora_repository_port import OperadoraRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.qualidade_servico_repository_port import QualidadeServicoRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.sla_repository_port import SLARepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusQualidadeServico, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.qualidade_servico import QualidadeServico

class QualidadeServicoService:

    def __init__(self, *, qualidade_repo: QualidadeServicoRepositoryPort, sla_repo: SLARepositoryPort, operadora_repo: OperadoraRepositoryPort, assinante_repo: AssinanteRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.qualidade_repo = qualidade_repo
        self.sla_repo = sla_repo
        self.operadora_repo = operadora_repo
        self.assinante_repo = assinante_repo
        self.request_service = request_service

    async def registrar_medicao(self, *, operadora_id: UUID, servico: TipoServico, data_medicao: date, disponibilidade_percentual: float, latencia_ms: float, jitter_ms: float, perda_pacotes_percentual: float, velocidade_download_mbps: float, velocidade_upload_mbps: float, assinante_id: UUID | None=None, sla_id: UUID | None=None, observacoes: str | None=None) -> QualidadeServico:
        operadora = await self.operadora_repo.get_by_id(operadora_id)
        if operadora is None:
            raise ValueError('Operadora nao encontrada para medicao de qualidade')
        if servico not in operadora.servicos_autorizados:
            raise ValueError('Servico informado nao esta autorizado para a operadora')
        if assinante_id is not None:
            assinante = await self.assinante_repo.get_by_id(assinante_id)
            if assinante is None:
                raise ValueError('Assinante nao encontrado')
            if assinante.operadora_id != operadora_id:
                raise ValueError('Assinante nao pertence a operadora informada')
        sla = None
        if sla_id is not None:
            sla = await self.sla_repo.get_by_id(sla_id)
            if sla is None:
                raise ValueError('SLA nao encontrado')
            if sla.operadora_id != operadora_id:
                raise ValueError('SLA nao pertence a operadora informada')
            if sla.servico != servico:
                raise ValueError('SLA nao corresponde ao servico informado')
        else:
            sla = await self.sla_repo.find_ativo_por_operadora_servico(operadora_id, servico)
            sla_id = sla.id if sla is not None else None
        codigo = await self.qualidade_repo.next_codigo()
        medicao = QualidadeServico.registrar(codigo_medicao=codigo, operadora_id=operadora_id, servico=servico, data_medicao=data_medicao, disponibilidade_percentual=disponibilidade_percentual, latencia_ms=latencia_ms, jitter_ms=jitter_ms, perda_pacotes_percentual=perda_pacotes_percentual, velocidade_download_mbps=velocidade_download_mbps, velocidade_upload_mbps=velocidade_upload_mbps, assinante_id=assinante_id, sla_id=sla_id, observacoes=observacoes)
        medicao.avaliar_conformidade(sla)
        saved = await self.qualidade_repo.save(medicao)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='MEDICAO_QUALIDADE_TELECOM', entity_id=saved.id, numero_processo=saved.codigo_medicao, metadata={'codigo_medicao': saved.codigo_medicao, 'operadora_id': str(saved.operadora_id), 'servico': saved.servico.value, 'status': saved.status.value}, citizen_id=assinante_id)
        return saved

    async def buscar_medicao(self, medicao_id: UUID) -> QualidadeServico:
        medicao = await self.qualidade_repo.get_by_id(medicao_id)
        if medicao is None:
            raise ValueError('Medicao de qualidade nao encontrada')
        return medicao

    async def listar_medicoes(self, *, operadora_id: UUID | None=None, assinante_id: UUID | None=None, status: StatusQualidadeServico | None=None) -> list[QualidadeServico]:
        if operadora_id is not None:
            return await self.qualidade_repo.list_by_operadora(operadora_id)
        if assinante_id is not None:
            return await self.qualidade_repo.list_by_assinante(assinante_id)
        if status is not None:
            return await self.qualidade_repo.list_by_status(status)
        return await self.qualidade_repo.list_all()

    async def atualizar_status(self, *, medicao_id: UUID, status: StatusQualidadeServico) -> QualidadeServico:
        medicao = await self.buscar_medicao(medicao_id)
        medicao.atualizar_status(status)
        return await self.qualidade_repo.save(medicao)

    async def remover_medicao(self, medicao_id: UUID) -> None:
        deleted = await self.qualidade_repo.delete(medicao_id)
        if not deleted:
            raise ValueError('Medicao de qualidade nao encontrada')