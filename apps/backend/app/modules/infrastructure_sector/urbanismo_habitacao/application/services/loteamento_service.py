from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.aguas_saneamento_service_port import AguasSaneamentoServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.ambiente_service_port import AmbienteServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.financas_service_port import FinancasServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.gestao_fundiaria_service_port import GestaoFundiariaServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.loteamento_repository_port import LoteamentoRepositoryPort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.obras_publicas_service_port import ObrasPublicasServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.transportes_service_port import TransportesServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.workflow_service_port import WorkflowServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusLoteamento, TipoLoteamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.loteamento import Loteamento
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import LoteamentoAlreadyExistsError, LoteamentoNotFoundError

class LoteamentoService:

    def __init__(self, *, loteamento_repo: LoteamentoRepositoryPort, gestao_fundiaria_adapter: GestaoFundiariaServicePort | None=None, ambiente_adapter: AmbienteServicePort | None=None, obras_publicas_adapter: ObrasPublicasServicePort | None=None, aguas_saneamento_adapter: AguasSaneamentoServicePort | None=None, transportes_adapter: TransportesServicePort | None=None, workflow_adapter: WorkflowServicePort | None=None, financas_adapter: FinancasServicePort | None=None) -> None:
        self._loteamento_repo = loteamento_repo
        self._gestao_fundiaria_adapter = gestao_fundiaria_adapter
        self._ambiente_adapter = ambiente_adapter
        self._obras_publicas_adapter = obras_publicas_adapter
        self._aguas_saneamento_adapter = aguas_saneamento_adapter
        self._transportes_adapter = transportes_adapter
        self._workflow_adapter = workflow_adapter
        self._financas_adapter = financas_adapter

    def has_gestao_fundiaria_adapter(self) -> bool:
        return self._gestao_fundiaria_adapter is not None

    def has_workflow_adapter(self) -> bool:
        return self._workflow_adapter is not None

    def has_financas_adapter(self) -> bool:
        return self._financas_adapter is not None

    def has_ambiente_adapter(self) -> bool:
        return self._ambiente_adapter is not None

    def has_obras_publicas_adapter(self) -> bool:
        return self._obras_publicas_adapter is not None

    def has_aguas_saneamento_adapter(self) -> bool:
        return self._aguas_saneamento_adapter is not None

    def has_transportes_adapter(self) -> bool:
        return self._transportes_adapter is not None

    async def criar(self, *, nome: str, tipo: TipoLoteamento, parcelamento_id: UUID, plano_diretor_id: UUID, zoneamento_id: UUID, provincia: str, area_total: Decimal, quantidade_lotes_prevista: int, municipio: str | None=None, area_lotes: Decimal | None=None, area_verde: Decimal | None=None, area_institucional: Decimal | None=None, data_inicio_prevista: date | None=None, data_fim_prevista: date | None=None, codigo_loteamento: str | None=None) -> Loteamento:
        if self._gestao_fundiaria_adapter:
            valido = await self._gestao_fundiaria_adapter.validar_imovel(parcelamento_id)
            if not valido:
                raise ValueError('Referencia fundiaria invalida para o loteamento')
        codigo = codigo_loteamento or await self._loteamento_repo.next_codigo()
        existente = await self._loteamento_repo.get_by_codigo(codigo)
        if existente:
            raise LoteamentoAlreadyExistsError('Ja existe loteamento com este codigo')
        item = Loteamento.criar(codigo_loteamento=codigo, nome=nome, tipo=tipo, parcelamento_id=parcelamento_id, plano_diretor_id=plano_diretor_id, zoneamento_id=zoneamento_id, provincia=provincia, area_total=area_total, quantidade_lotes_prevista=quantidade_lotes_prevista, municipio=municipio, area_lotes=area_lotes, area_verde=area_verde, area_institucional=area_institucional, data_inicio_prevista=data_inicio_prevista, data_fim_prevista=data_fim_prevista)
        if self._financas_adapter:
            taxa = await self._financas_adapter.calcular_taxa_loteamento(area_total=area_total, quantidade_lotes=quantidade_lotes_prevista)
            item.observacoes = f'taxa_loteamento:{taxa}'
        saved = await self._loteamento_repo.save(item)
        if self._workflow_adapter:
            workflow_id = await self._workflow_adapter.iniciar_fluxo(entidade='urbanismo_loteamento', referencia_id=saved.id, contexto={'codigo_loteamento': saved.codigo_loteamento})
            sufixo = f'workflow_id:{workflow_id}'
            saved.observacoes = f'{saved.observacoes}|{sufixo}' if saved.observacoes else sufixo
            saved = await self._loteamento_repo.save(saved)
        return saved

    async def aprovar(self, codigo_loteamento: str) -> Loteamento:
        item = await self._obter_ou_erro(codigo_loteamento)
        if self._ambiente_adapter:
            licenca_ok = await self._ambiente_adapter.validar_licenca_ambiental(item.zoneamento_id)
            if not licenca_ok:
                raise ValueError('Pendencia ambiental impede aprovacao do loteamento')
        if self._obras_publicas_adapter:
            obra_ok = await self._obras_publicas_adapter.validar_obra(item.parcelamento_id)
            if not obra_ok:
                raise ValueError('Pendencia de obras publicas impede aprovacao do loteamento')
        if self._aguas_saneamento_adapter:
            agua_ok = await self._aguas_saneamento_adapter.validar_capacidade_atendimento(zoneamento_id=item.zoneamento_id, quantidade_lotes=item.quantidade_lotes_prevista)
            if not agua_ok:
                raise ValueError('Capacidade de agua e saneamento insuficiente para aprovacao')
        if self._transportes_adapter:
            impacto_ok = await self._transportes_adapter.validar_impacto_viario(zoneamento_id=item.zoneamento_id, quantidade_lotes=item.quantidade_lotes_prevista)
            if not impacto_ok:
                raise ValueError('Impacto viario excede limite para aprovacao')
        item.aprovar()
        saved = await self._loteamento_repo.save(item)
        if self._workflow_adapter:
            await self._workflow_adapter.registrar_evento(workflow_id=saved.codigo_loteamento, evento='loteamento_aprovado', payload={'status': saved.status.value})
        return saved

    async def iniciar_implantacao(self, codigo_loteamento: str, *, data_inicio_real: date) -> Loteamento:
        item = await self._obter_ou_erro(codigo_loteamento)
        item.iniciar_implantacao(data_inicio_real=data_inicio_real)
        return await self._loteamento_repo.save(item)

    async def registrar_implantacao(self, codigo_loteamento: str, *, quantidade_lotes_implantada: int) -> Loteamento:
        item = await self._obter_ou_erro(codigo_loteamento)
        item.registrar_implantacao(quantidade_lotes_implantada=quantidade_lotes_implantada)
        return await self._loteamento_repo.save(item)

    async def concluir(self, codigo_loteamento: str, *, data_fim_real: date) -> Loteamento:
        item = await self._obter_ou_erro(codigo_loteamento)
        item.concluir(data_fim_real=data_fim_real)
        return await self._loteamento_repo.save(item)

    async def suspender(self, codigo_loteamento: str, *, motivo: str) -> Loteamento:
        item = await self._obter_ou_erro(codigo_loteamento)
        item.suspender(motivo=motivo)
        return await self._loteamento_repo.save(item)

    async def retomar(self, codigo_loteamento: str) -> Loteamento:
        item = await self._obter_ou_erro(codigo_loteamento)
        item.retomar()
        return await self._loteamento_repo.save(item)

    async def cancelar(self, codigo_loteamento: str, *, motivo: str) -> Loteamento:
        item = await self._obter_ou_erro(codigo_loteamento)
        item.cancelar(motivo=motivo)
        return await self._loteamento_repo.save(item)

    async def obter_por_codigo(self, codigo_loteamento: str) -> Loteamento:
        return await self._obter_ou_erro(codigo_loteamento)

    async def listar(self, *, status: StatusLoteamento | None=None, tipo: TipoLoteamento | None=None, provincia: str | None=None) -> list[Loteamento]:
        return await self._loteamento_repo.list(status=status, tipo=tipo, provincia=provincia)

    async def _obter_ou_erro(self, codigo_loteamento: str) -> Loteamento:
        item = await self._loteamento_repo.get_by_codigo(codigo_loteamento)
        if not item:
            raise LoteamentoNotFoundError('Loteamento nao encontrado')
        return item