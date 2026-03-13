from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.resources.pescas.industrial.application.ports.inspecao_sanitaria_industrial_repository_port import InspecaoSanitariaIndustrialRepositoryPort
from apps.backend.app.modules.resources.pescas.industrial.application.ports.lote_producao_repository_port import LoteProducaoRepositoryPort
from apps.backend.app.modules.resources.pescas.industrial.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.resources.pescas.industrial.application.ports.unidade_processamento_repository_port import UnidadeProcessamentoRepositoryPort
from apps.backend.app.modules.resources.pescas.industrial.domain.enums import StatusInspecao, TipoSeloInspecao
from apps.backend.app.modules.resources.pescas.industrial.domain.models.inspecao_sanitaria_industrial import InspecaoSanitariaIndustrial

class InspecaoIndustrialService:

    def __init__(self, *, inspecao_repo: InspecaoSanitariaIndustrialRepositoryPort, unidade_repo: UnidadeProcessamentoRepositoryPort, lote_repo: LoteProducaoRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.inspecao_repo = inspecao_repo
        self.unidade_repo = unidade_repo
        self.lote_repo = lote_repo
        self.request_service = request_service

    async def agendar_inspecao(self, *, unidade_processamento_id: UUID, data_agendada: date, selo_inspecao: TipoSeloInspecao, fiscal_id: UUID | None=None, lote_producao_id: UUID | None=None, observacoes: str | None=None) -> InspecaoSanitariaIndustrial:
        await self._validar_unidade(unidade_processamento_id)
        if lote_producao_id is not None:
            lote = await self.lote_repo.get_by_id(lote_producao_id)
            if lote is None:
                raise ValueError('Lote de producao nao encontrado')
            if lote.unidade_processamento_id != unidade_processamento_id:
                raise ValueError('Lote nao pertence a unidade informada')
        codigo = await self.inspecao_repo.next_codigo()
        inspecao = InspecaoSanitariaIndustrial.agendar(codigo_inspecao=codigo, unidade_processamento_id=unidade_processamento_id, data_agendada=data_agendada, selo_inspecao=selo_inspecao, fiscal_id=fiscal_id, lote_producao_id=lote_producao_id, observacoes=observacoes)
        saved = await self.inspecao_repo.save(inspecao)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='AGENDAMENTO_INSPECAO_SANITARIA', entity_id=saved.id, metadata={'codigo_inspecao': saved.codigo_inspecao, 'status': saved.status.value, 'selo': saved.selo_inspecao.value}, numero_processo=saved.codigo_inspecao, citizen_id=fiscal_id)
        return saved

    async def buscar_inspecao(self, inspecao_id: UUID) -> InspecaoSanitariaIndustrial:
        item = await self.inspecao_repo.get_by_id(inspecao_id)
        if not item:
            raise ValueError('Inspecao sanitaria nao encontrada')
        return item

    async def listar_inspecoes(self, *, unidade_processamento_id: UUID | None=None, status: StatusInspecao | None=None, lote_producao_id: UUID | None=None, data_inicio: date | None=None, data_fim: date | None=None) -> list[InspecaoSanitariaIndustrial]:
        if unidade_processamento_id is not None:
            return await self.inspecao_repo.list_by_unidade(unidade_processamento_id)
        if status is not None:
            return await self.inspecao_repo.list_by_status(status)
        if lote_producao_id is not None:
            return await self.inspecao_repo.list_by_lote(lote_producao_id)
        if data_inicio is not None and data_fim is not None:
            return await self.inspecao_repo.list_by_periodo(data_inicio, data_fim)
        return await self.inspecao_repo.list_all()

    async def atualizar_status(self, *, inspecao_id: UUID, status: StatusInspecao, pontuacao: int | None=None, aprovada: bool | None=None, inconformidades: list[str] | None=None, observacoes: str | None=None) -> InspecaoSanitariaIndustrial:
        item = await self.buscar_inspecao(inspecao_id)
        if status == StatusInspecao.EM_ANDAMENTO:
            item.iniciar()
        elif status in {StatusInspecao.APROVADA, StatusInspecao.REPROVADA}:
            if pontuacao is None:
                raise ValueError('Pontuacao e obrigatoria para conclusao')
            if aprovada is None:
                aprovada = status == StatusInspecao.APROVADA
            item.concluir(pontuacao=pontuacao, aprovada=aprovada, inconformidades=inconformidades, observacoes=observacoes)
        else:
            item.atualizar_status(status, observacoes)
        return await self.inspecao_repo.save(item)

    async def remover_inspecao(self, inspecao_id: UUID) -> None:
        deleted = await self.inspecao_repo.delete(inspecao_id)
        if not deleted:
            raise ValueError('Inspecao sanitaria nao encontrada')

    async def _validar_unidade(self, unidade_processamento_id: UUID) -> None:
        unidade = await self.unidade_repo.get_by_id(unidade_processamento_id)
        if unidade is None:
            raise ValueError('Unidade de processamento nao encontrada')