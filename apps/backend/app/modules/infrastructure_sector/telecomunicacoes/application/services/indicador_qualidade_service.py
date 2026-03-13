from __future__ import annotations
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.indicador_qualidade_repository_port import IndicadorQualidadeRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.operadora_repository_port import OperadoraRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.qualidade_servico_repository_port import QualidadeServicoRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusIndicadorQualidade
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.indicador_qualidade import IndicadorQualidade
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.qualidade_servico import QualidadeServico

class IndicadorQualidadeService:

    def __init__(self, *, indicador_repo: IndicadorQualidadeRepositoryPort, qualidade_repo: QualidadeServicoRepositoryPort, operadora_repo: OperadoraRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.indicador_repo = indicador_repo
        self.qualidade_repo = qualidade_repo
        self.operadora_repo = operadora_repo
        self.request_service = request_service

    async def gerar_indicador_operadora(self, *, operadora_id: UUID, referencia_ano: int, referencia_mes: int, observacoes: str | None=None) -> IndicadorQualidade:
        operadora = await self.operadora_repo.get_by_id(operadora_id)
        if operadora is None:
            raise ValueError('Operadora nao encontrada para geracao de indicador')
        medicoes = await self.qualidade_repo.list_by_operadora_periodo(operadora_id=operadora_id, referencia_ano=referencia_ano, referencia_mes=referencia_mes)
        if not medicoes:
            raise ValueError('Nao existem medicoes no periodo informado para gerar indicador')
        existente = await self.indicador_repo.get_by_operadora_periodo(operadora_id=operadora_id, referencia_ano=referencia_ano, referencia_mes=referencia_mes)
        codigo = existente.codigo_indicador if existente is not None else await self.indicador_repo.next_codigo()
        indicador = self._build_indicador(codigo=codigo, operadora_id=operadora_id, referencia_ano=referencia_ano, referencia_mes=referencia_mes, medicoes=medicoes, observacoes=observacoes)
        if existente is not None:
            indicador.id = existente.id
        saved = await self.indicador_repo.save(indicador)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='GERACAO_INDICADOR_QUALIDADE_TELECOM', entity_id=saved.id, numero_processo=saved.codigo_indicador, metadata={'codigo_indicador': saved.codigo_indicador, 'operadora_id': str(saved.operadora_id), 'referencia': f'{saved.referencia_ano:04d}-{saved.referencia_mes:02d}', 'status': saved.status.value})
        return saved

    async def buscar_indicador(self, indicador_id: UUID) -> IndicadorQualidade:
        indicador = await self.indicador_repo.get_by_id(indicador_id)
        if indicador is None:
            raise ValueError('Indicador de qualidade nao encontrado')
        return indicador

    async def listar_indicadores(self, *, operadora_id: UUID | None=None, status: StatusIndicadorQualidade | None=None) -> list[IndicadorQualidade]:
        if operadora_id is not None:
            return await self.indicador_repo.list_by_operadora(operadora_id)
        if status is not None:
            return await self.indicador_repo.list_by_status(status)
        return await self.indicador_repo.list_all()

    async def remover_indicador(self, indicador_id: UUID) -> None:
        deleted = await self.indicador_repo.delete(indicador_id)
        if not deleted:
            raise ValueError('Indicador de qualidade nao encontrado')

    @staticmethod
    def _build_indicador(*, codigo: str, operadora_id: UUID, referencia_ano: int, referencia_mes: int, medicoes: list[QualidadeServico], observacoes: str | None) -> IndicadorQualidade:
        total = len(medicoes)
        disponibilidade_media = sum((item.disponibilidade_percentual for item in medicoes)) / total
        latencia_media = sum((item.latencia_ms for item in medicoes)) / total
        jitter_medio = sum((item.jitter_ms for item in medicoes)) / total
        perda_media = sum((item.perda_pacotes_percentual for item in medicoes)) / total
        conformes = sum((1 for item in medicoes if item.status.value == 'conforme'))
        conformidade_percentual = conformes * 100.0 / total
        return IndicadorQualidade.registrar(codigo_indicador=codigo, operadora_id=operadora_id, referencia_ano=referencia_ano, referencia_mes=referencia_mes, total_medicoes=total, disponibilidade_media_percentual=disponibilidade_media, latencia_media_ms=latencia_media, jitter_medio_ms=jitter_medio, perda_pacotes_media_percentual=perda_media, conformidade_percentual=conformidade_percentual, observacoes=observacoes)