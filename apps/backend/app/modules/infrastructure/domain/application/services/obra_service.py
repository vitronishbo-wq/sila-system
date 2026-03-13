from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.infrastructure.application.ports.aguas_saneamento_service_port import AguasSaneamentoServicePort
from apps.backend.app.modules.infrastructure.application.ports.ambiente_service_port import AmbienteServicePort
from apps.backend.app.modules.infrastructure.application.ports.financas_publicas_service_port import FinancasPublicasServicePort
from apps.backend.app.modules.infrastructure.application.ports.gestao_fundiaria_service_port import GestaoFundiariaServicePort
from apps.backend.app.modules.infrastructure.application.ports.obra_repository_port import ObraRepositoryPort
from apps.backend.app.modules.infrastructure.application.ports.outbox_repository_port import OutboxRepositoryPort
from apps.backend.app.modules.infrastructure.infrastructure.eventsourcing.event_store_repository import SQLAlchemyEventStoreRepository
from apps.backend.app.modules.infrastructure.infrastructure.multi_region.global_id import generate_global_id
from apps.backend.app.modules.infrastructure.application.ports.service_requests_service_port import ServiceRequestsServicePort
from apps.backend.app.modules.infrastructure.application.ports.transportes_service_port import TransportesServicePort
from apps.backend.app.modules.infrastructure.application.ports.urbanismo_habitacao_service_port import UrbanismoHabitacaoServicePort
from apps.backend.app.modules.infrastructure.application.ports.workflow_service_port import WorkflowServicePort
from apps.backend.app.modules.infrastructure.application.events.definitions import AditivoAssinadoEvent, MedicaoAprovadaEvent, ObraConcluidaEvent, ObraCriadaEvent, ObraIniciadaEvent
from apps.backend.app.modules.infrastructure.application.eventsourcing.obra_event_aggregate import rehydrate_obra
from apps.backend.app.modules.infrastructure.domain.enums import NaturezaObra, StatusObra, TipoObra
from apps.backend.app.modules.infrastructure.domain.models.aditivo_contratual import AditivoContratual
from apps.backend.app.modules.infrastructure.domain.models.fiscalizacao_obra import FiscalizacaoObra
from apps.backend.app.modules.infrastructure.domain.models.medicao_obra import MedicaoObra
from apps.backend.app.modules.infrastructure.domain.models.obra import Obra
from apps.backend.app.modules.infrastructure.domain.models.termo_recebimento import TermoRecebimento
from apps.backend.app.modules.infrastructure.domain.exceptions import ObraAlreadyExistsError, ObraNotFoundError

class ObraService:

    def __init__(self, *, obra_repo: ObraRepositoryPort, gestao_fundiaria_adapter: GestaoFundiariaServicePort | None=None, financas_publicas_adapter: FinancasPublicasServicePort | None=None, ambiente_adapter: AmbienteServicePort | None=None, urbanismo_habitacao_adapter: UrbanismoHabitacaoServicePort | None=None, transportes_adapter: TransportesServicePort | None=None, aguas_saneamento_adapter: AguasSaneamentoServicePort | None=None, workflow_adapter: WorkflowServicePort | None=None, service_requests_adapter: ServiceRequestsServicePort | None=None, outbox_repo: OutboxRepositoryPort | None=None, event_store_repo: SQLAlchemyEventStoreRepository | None=None) -> None:
        self._obra_repo = obra_repo
        self._gestao_fundiaria_adapter = gestao_fundiaria_adapter
        self._financas_publicas_adapter = financas_publicas_adapter
        self._ambiente_adapter = ambiente_adapter
        self._urbanismo_habitacao_adapter = urbanismo_habitacao_adapter
        self._transportes_adapter = transportes_adapter
        self._aguas_saneamento_adapter = aguas_saneamento_adapter
        self._workflow_adapter = workflow_adapter
        self._service_requests_adapter = service_requests_adapter
        self._outbox_repo = outbox_repo
        self._event_store_repo = event_store_repo

    def has_urbanismo_habitacao_adapter(self) -> bool:
        return self._outbox_repo is not None or self._urbanismo_habitacao_adapter is not None

    def has_workflow_adapter(self) -> bool:
        return self._outbox_repo is not None or self._workflow_adapter is not None

    def has_service_requests_adapter(self) -> bool:
        return self._outbox_repo is not None or self._service_requests_adapter is not None

    def has_ambiente_adapter(self) -> bool:
        return self._outbox_repo is not None or self._ambiente_adapter is not None

    def has_transportes_adapter(self) -> bool:
        return self._outbox_repo is not None or self._transportes_adapter is not None

    def has_aguas_saneamento_adapter(self) -> bool:
        return self._outbox_repo is not None or self._aguas_saneamento_adapter is not None

    async def criar(self, *, nome: str, tipo: TipoObra, natureza: NaturezaObra, orgao_responsavel_id: UUID, orgao_responsavel_tipo: str, valor_orcado: Decimal, data_inicio_prevista: date, data_fim_prevista: date, endereco: str, bairro: str, municipio: str, provincia: str, codigo_obra: str | None=None, descricao: str | None=None, tenant_id: str='default', correlation_id: str | None=None) -> Obra:
        codigo = codigo_obra or await self._obra_repo.next_codigo()
        existente = await self._obra_repo.get_by_codigo(codigo)
        if existente:
            raise ObraAlreadyExistsError('Ja existe obra com este codigo')
        if self._outbox_repo is None and self._urbanismo_habitacao_adapter:
            conforme = await self._urbanismo_habitacao_adapter.validar_conformidade_urbanistica(endereco=endereco, bairro=bairro, municipio=municipio, provincia=provincia, tipo_obra=tipo)
            if not conforme:
                raise ValueError('Conformidade urbanistica invalida para criacao da obra')
        item = Obra.criar(codigo_obra=codigo, nome=nome, tipo=tipo, natureza=natureza, orgao_responsavel_id=orgao_responsavel_id, orgao_responsavel_tipo=orgao_responsavel_tipo, valor_orcado=valor_orcado, data_inicio_prevista=data_inicio_prevista, data_fim_prevista=data_fim_prevista, endereco=endereco, bairro=bairro, municipio=municipio, provincia=provincia, descricao=descricao)
        if self._outbox_repo is None and self._financas_publicas_adapter:
            reservado = await self._financas_publicas_adapter.reservar_dotacao(item.orgao_responsavel_id, item.valor_orcado)
            if not reservado:
                raise ValueError('Dotacao orcamentaria indisponivel para criacao da obra')
        saved = await self._obra_repo.save(item)
        if self._outbox_repo is None and self._service_requests_adapter:
            solicitacao_id = await self._service_requests_adapter.abrir_solicitacao({'tipo': 'obra_publica', 'codigo_obra': saved.codigo_obra, 'municipio': saved.municipio, 'provincia': saved.provincia})
            sufixo = f'service_request_id:{solicitacao_id}'
            saved.observacoes = f'{saved.observacoes}|{sufixo}' if saved.observacoes else sufixo
            saved = await self._obra_repo.save(saved)
        if self._outbox_repo is None and self._workflow_adapter:
            workflow_id = await self._workflow_adapter.iniciar_fluxo(entidade='obras_publicas_obra', referencia_id=saved.id, contexto={'codigo_obra': saved.codigo_obra})
            sufixo = f'workflow_id:{workflow_id}'
            saved.observacoes = f'{saved.observacoes}|{sufixo}' if saved.observacoes else sufixo
            saved.registrar_evento_auditoria(evento='workflow_iniciado', payload={'workflow_id': workflow_id})
            saved = await self._obra_repo.save(saved)
        await self._emit_outbox_event(tenant_id=tenant_id, correlation_id=correlation_id, aggregate_type='Obra', aggregate_id=str(saved.id), event=ObraCriadaEvent.build(obra_id=saved.id, codigo_obra=saved.codigo_obra, municipio=saved.municipio, provincia=saved.provincia, valor_orcado=saved.valor_orcado))
        return saved

    async def iniciar_licitacao(self, codigo_obra: str) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        item.iniciar_licitacao()
        item.registrar_evento_auditoria(evento='iniciar_licitacao')
        saved = await self._obra_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='obra_em_licitacao', payload={'status': saved.status.value})
        return saved

    async def contratar(self, codigo_obra: str, *, contrato_id: UUID, empreiteira_id: UUID, valor: Decimal) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        if self._outbox_repo is None and self._financas_publicas_adapter:
            reservado = await self._financas_publicas_adapter.reservar_dotacao(item.orgao_responsavel_id, valor)
            if not reservado:
                raise ValueError('Dotacao orcamentaria insuficiente para contratacao')
        item.contratar(contrato_id=contrato_id, empreiteira_id=empreiteira_id, valor=valor)
        item.registrar_evento_auditoria(evento='contratacao', payload={'contrato_id': str(contrato_id), 'valor': str(valor)})
        saved = await self._obra_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='obra_contratada', payload={'status': saved.status.value, 'valor_contratado': str(saved.valor_contratado)})
        return saved

    async def iniciar_execucao(self, codigo_obra: str, *, data_inicio: date, tenant_id: str='default', correlation_id: str | None=None) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        if self._outbox_repo is None and self._ambiente_adapter:
            licenca_ok = await self._ambiente_adapter.validar_licenca_ambiental(item.id)
            if not licenca_ok:
                raise ValueError('Licenca ambiental invalida para inicio de execucao')
        if self._outbox_repo is None and self._transportes_adapter:
            impacto_ok = await self._transportes_adapter.validar_impacto_viario(municipio=item.municipio, provincia=item.provincia, tipo_obra=item.tipo)
            if not impacto_ok:
                raise ValueError('Impacto viario impede inicio de execucao da obra')
        if self._outbox_repo is None and self._aguas_saneamento_adapter:
            rede_ok = await self._aguas_saneamento_adapter.validar_capacidade_rede(municipio=item.municipio, provincia=item.provincia, tipo_obra=item.tipo)
            if not rede_ok:
                raise ValueError('Capacidade de aguas e saneamento insuficiente para inicio de execucao')
        item.iniciar_execucao(data_inicio)
        item.registrar_evento_auditoria(evento='iniciar_execucao', payload={'data_inicio': data_inicio.isoformat()})
        saved = await self._obra_repo.save(item)
        if self._outbox_repo is not None:
            await self._emit_outbox_event(tenant_id=tenant_id, correlation_id=correlation_id, aggregate_type='Obra', aggregate_id=str(saved.id), event=ObraIniciadaEvent.build(obra_id=saved.id, codigo_obra=saved.codigo_obra, data_inicio=data_inicio))
        else:
            await self._registrar_evento_workflow(saved, evento='obra_em_execucao', payload={'status': saved.status.value})
        return saved

    async def atualizar_progresso(self, codigo_obra: str, *, percentual: Decimal) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        item.atualizar_progresso(percentual)
        item.registrar_evento_auditoria(evento='atualizar_progresso', payload={'percentual_executado': str(item.percentual_executado)})
        saved = await self._obra_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='obra_progresso_atualizado', payload={'percentual_executado': str(saved.percentual_executado)})
        return saved

    async def registrar_medicao(self, codigo_obra: str, *, valor: Decimal) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        item.registrar_medicao(valor)
        item.registrar_evento_auditoria(evento='medicao_valor', payload={'valor_medido': str(valor)})
        saved = await self._obra_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='obra_medicao_registrada', payload={'valor_medido': str(valor), 'valor_executado': str(saved.valor_executado)})
        return saved

    async def registrar_medicao_detalhada(self, codigo_obra: str, *, periodo_referencia: str, valor_medido: Decimal, percentual_executado: Decimal, fiscal_id: UUID, documentos: list[str] | None=None, observacoes: str | None=None, data_medicao: date | None=None, tenant_id: str='default', correlation_id: str | None=None) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        medicao = MedicaoObra.registrar(periodo_referencia=periodo_referencia, valor_medido=valor_medido, percentual_executado=percentual_executado, fiscal_id=fiscal_id, documentos=documentos, observacoes=observacoes, data_medicao=data_medicao)
        item.registrar_medicao_detalhada(medicao)
        item.registrar_evento_auditoria(evento='medicao_detalhada', payload={'medicao_id': str(medicao.id), 'periodo_referencia': medicao.periodo_referencia})
        saved = await self._obra_repo.save(item)
        if self._outbox_repo is not None:
            await self._emit_outbox_event(tenant_id=tenant_id, correlation_id=correlation_id, aggregate_type='Obra', aggregate_id=str(saved.id), event=MedicaoAprovadaEvent.build(obra_id=saved.id, codigo_obra=saved.codigo_obra, medicao_id=medicao.id, valor_medido=medicao.valor_medido, percentual_executado=saved.percentual_executado))
        else:
            await self._registrar_evento_workflow(saved, evento='obra_medicao_detalhada_registrada', payload={'medicao_id': str(medicao.id), 'percentual_executado': str(saved.percentual_executado)})
        return saved

    async def registrar_aditivo(self, codigo_obra: str, *, tipo: str, justificativa: str, valor_aditivo: Decimal=Decimal('0'), prazo_adicional_dias: int=0, data_assinatura: date | None=None, tenant_id: str='default', correlation_id: str | None=None) -> Obra:
        from apps.backend.app.modules.infrastructure.domain.enums import TipoAditivo
        item = await self._obter_ou_erro(codigo_obra)
        aditivo = AditivoContratual.registrar(tipo=TipoAditivo(tipo), justificativa=justificativa, valor_aditivo=valor_aditivo, prazo_adicional_dias=prazo_adicional_dias, data_assinatura=data_assinatura)
        item.registrar_aditivo(aditivo)
        item.registrar_evento_auditoria(evento='aditivo_contratual', payload={'aditivo_id': str(aditivo.id), 'tipo': aditivo.tipo.value})
        saved = await self._obra_repo.save(item)
        if self._outbox_repo is not None:
            await self._emit_outbox_event(tenant_id=tenant_id, correlation_id=correlation_id, aggregate_type='Obra', aggregate_id=str(saved.id), event=AditivoAssinadoEvent.build(obra_id=saved.id, codigo_obra=saved.codigo_obra, aditivo_id=aditivo.id, tipo=aditivo.tipo.value, valor_adicional=aditivo.valor_aditivo, prazo_adicional_dias=aditivo.prazo_adicional_dias))
        else:
            await self._registrar_evento_workflow(saved, evento='obra_aditivo_registrado', payload={'aditivo_id': str(aditivo.id), 'tipo': aditivo.tipo.value})
        return saved

    async def registrar_fiscalizacao(self, codigo_obra: str, *, fiscal_id: UUID, conformidade: bool, apontamentos: str, recomendacoes: str | None=None, data_fiscalizacao: date | None=None) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        fiscalizacao = FiscalizacaoObra.registrar(fiscal_id=fiscal_id, conformidade=conformidade, apontamentos=apontamentos, recomendacoes=recomendacoes, data_fiscalizacao=data_fiscalizacao)
        item.registrar_fiscalizacao(fiscalizacao)
        item.registrar_evento_auditoria(evento='fiscalizacao_obra', payload={'fiscalizacao_id': str(fiscalizacao.id), 'conformidade': conformidade})
        saved = await self._obra_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='obra_fiscalizacao_registrada', payload={'fiscalizacao_id': str(fiscalizacao.id), 'conformidade': conformidade})
        return saved

    async def registrar_pagamento(self, codigo_obra: str, *, valor: Decimal) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        item.registrar_pagamento(valor)
        item.registrar_evento_auditoria(evento='registrar_pagamento', payload={'valor_pago': str(valor)})
        saved = await self._obra_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='obra_pagamento_registrado', payload={'valor_pago': str(valor), 'valor_pago_acumulado': str(saved.valor_pago)})
        return saved

    async def suspender(self, codigo_obra: str, *, motivo: str) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        item.suspender(motivo)
        item.registrar_evento_auditoria(evento='suspender_obra', payload={'motivo': motivo})
        saved = await self._obra_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='obra_suspensa', payload={'motivo': motivo})
        return saved

    async def retomar(self, codigo_obra: str) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        item.retomar()
        item.registrar_evento_auditoria(evento='retomar_obra')
        saved = await self._obra_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='obra_retornada_execucao', payload={'status': saved.status.value})
        return saved

    async def concluir(self, codigo_obra: str, *, data_conclusao: date, tenant_id: str='default', correlation_id: str | None=None) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        item.concluir(data_conclusao)
        item.registrar_evento_auditoria(evento='concluir_obra', payload={'data_conclusao': data_conclusao.isoformat()})
        saved = await self._obra_repo.save(item)
        if self._outbox_repo is not None:
            await self._emit_outbox_event(tenant_id=tenant_id, correlation_id=correlation_id, aggregate_type='Obra', aggregate_id=str(saved.id), event=ObraConcluidaEvent.build(obra_id=saved.id, codigo_obra=saved.codigo_obra, data_conclusao=data_conclusao))
        else:
            await self._registrar_evento_workflow(saved, evento='obra_concluida', payload={'data_conclusao': data_conclusao.isoformat()})
        return saved

    async def entregar(self, codigo_obra: str, *, data_entrega: date) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        item.entregar(data_entrega)
        item.registrar_evento_auditoria(evento='entregar_obra', payload={'data_entrega': data_entrega.isoformat()})
        saved = await self._obra_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='obra_entregue', payload={'data_entrega': data_entrega.isoformat()})
        return saved

    async def registrar_termo_recebimento(self, codigo_obra: str, *, tipo: str, responsavel_id: UUID, data_termo: date | None=None, observacoes: str | None=None) -> Obra:
        item = await self._obter_ou_erro(codigo_obra)
        termo = TermoRecebimento.registrar(tipo=tipo, responsavel_id=responsavel_id, data_termo=data_termo, observacoes=observacoes)
        item.registrar_termo_recebimento(termo)
        item.registrar_evento_auditoria(evento='termo_recebimento', payload={'termo_id': str(termo.id), 'tipo': termo.tipo})
        saved = await self._obra_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='obra_termo_recebimento_registrado', payload={'termo_id': str(termo.id), 'tipo': termo.tipo})
        return saved

    async def obter_por_codigo(self, codigo_obra: str) -> Obra:
        return await self._obter_ou_erro(codigo_obra)

    async def listar(self, *, status: StatusObra | None=None, orgao_responsavel_id: UUID | None=None, municipio: str | None=None, provincia: str | None=None) -> list[Obra]:
        return await self._obra_repo.list(status=status, orgao_responsavel_id=orgao_responsavel_id, municipio=municipio, provincia=provincia)

    async def obter_event_stream(self, codigo_obra: str, *, tenant_id: str | None=None) -> list[dict]:
        item = await self._obter_ou_erro(codigo_obra)
        if self._event_store_repo is None:
            return []
        entries = await self._event_store_repo.list_events_for_aggregate(aggregate_id=str(item.id), tenant_id=tenant_id)
        return [{'id': str(entry.id), 'aggregate_id': entry.aggregate_id, 'aggregate_type': entry.aggregate_type, 'event_type': entry.event_type, 'event_data': entry.event_data, 'version': entry.version, 'tenant_id': entry.tenant_id, 'region_code': entry.region_code, 'correlation_id': entry.correlation_id, 'created_at': entry.created_at.isoformat() if entry.created_at else None} for entry in entries]

    async def rehidratar_estado_obra(self, codigo_obra: str, *, tenant_id: str | None=None) -> dict:
        stream = await self.obter_event_stream(codigo_obra, tenant_id=tenant_id)
        if not stream:
            return {}
        obra_id = str(stream[0]['aggregate_id'])
        state = rehydrate_obra(obra_id, stream)
        return {'obra_id': state.obra_id, 'codigo_obra': state.codigo_obra, 'status': state.status, 'valor_total': str(state.valor_total), 'valor_executado': str(state.valor_executado), 'event_count': len(stream)}

    async def _obter_ou_erro(self, codigo_obra: str) -> Obra:
        item = await self._obra_repo.get_by_codigo(codigo_obra)
        if not item:
            raise ObraNotFoundError('Obra nao encontrada')
        return item

    async def _registrar_evento_workflow(self, item: Obra, *, evento: str, payload: dict) -> None:
        if self._outbox_repo is not None:
            return
        if not self._workflow_adapter:
            return
        await self._workflow_adapter.registrar_evento(workflow_id=item.codigo_obra, evento=evento, payload=payload)

    async def _emit_outbox_event(self, *, tenant_id: str, correlation_id: str | None, aggregate_type: str, aggregate_id: str, event) -> None:
        resolved_correlation = correlation_id or generate_global_id()
        payload = dict(event.to_payload() or {})
        if self._event_store_repo is not None:
            await self._event_store_repo.append_event(aggregate_id=aggregate_id, aggregate_type=aggregate_type, event_type=str(event.event_name), event_data=payload, tenant_id=tenant_id or 'default', correlation_id=resolved_correlation, expected_version=None)
        if self._outbox_repo is None:
            return
        await self._outbox_repo.save(tenant_id=tenant_id or 'default', aggregate_type=aggregate_type, aggregate_id=aggregate_id, event=event, correlation_id=resolved_correlation)
