from __future__ import annotations
from apps.backend.app.modules.energy.application.events.bus import event_bus
from apps.backend.app.modules.energy.application.events.definitions import FaturaGeradaEvent, LeituraRealizadaEvent, QualidadeInconformeEvent
from apps.backend.app.modules.energy.application.handlers import AuditoriaHandler, FaturamentoHandler
from apps.backend.app.modules.energy.application.services import CentralGeradoraService, ConsumoService, FaturamentoService, GeracaoService, LinhaTransmissaoService, SubestacaoService, UsinaService
from apps.backend.app.modules.energy.infrastructure.adapters import ANEELAdapter, ONSAdapter
from apps.backend.app.modules.energy.infrastructure.persistence import SQLAlchemyOutboxRepository
from apps.backend.app.modules.energy.infrastructure.repositories import SQLAlchemyCentralGeradoraRepository, SQLAlchemyConsumoRepository, SQLAlchemyFaturaRepository, SQLAlchemyLinhaTransmissaoRepository, SQLAlchemySubestacaoRepository, SQLAlchemyUsinaRepository
from apps.backend.app.modules.energy.domain.workers import OutboxWorker
usina_repo_singleton = SQLAlchemyUsinaRepository()
usina_service_singleton = UsinaService(usina_repo=usina_repo_singleton)
central_geradora_repo_singleton = SQLAlchemyCentralGeradoraRepository()
central_geradora_service_singleton = CentralGeradoraService(repository=central_geradora_repo_singleton)
subestacao_repo_singleton = SQLAlchemySubestacaoRepository()
subestacao_service_singleton = SubestacaoService(repository=subestacao_repo_singleton)
linha_transmissao_repo_singleton = SQLAlchemyLinhaTransmissaoRepository()
linha_transmissao_service_singleton = LinhaTransmissaoService(repository=linha_transmissao_repo_singleton)
geracao_service_singleton = GeracaoService(central_repo=central_geradora_repo_singleton, sub_repo=subestacao_repo_singleton, linha_repo=linha_transmissao_repo_singleton)
consumo_repo_singleton = SQLAlchemyConsumoRepository()
fatura_repo_singleton = SQLAlchemyFaturaRepository()
outbox_repo_singleton = SQLAlchemyOutboxRepository()
ons_adapter_singleton = ONSAdapter()
aneel_adapter_singleton = ANEELAdapter()
consumo_service_singleton = ConsumoService(consumo_repo=consumo_repo_singleton, outbox_repo=outbox_repo_singleton)
faturamento_service_singleton = FaturamentoService(fatura_repo=fatura_repo_singleton, consumo_repo=consumo_repo_singleton, outbox_repo=outbox_repo_singleton, ons_adapter=ons_adapter_singleton)
faturamento_handler_singleton = FaturamentoHandler(faturamento_service=faturamento_service_singleton)
auditoria_handler_singleton = AuditoriaHandler(aneel_adapter=aneel_adapter_singleton)
outbox_worker_singleton = OutboxWorker(outbox_repo=outbox_repo_singleton, event_bus=event_bus)
_subscriptions_configured = False

def _configure_subscriptions() -> None:
    global _subscriptions_configured
    if _subscriptions_configured:
        return
    event_bus.subscribe(LeituraRealizadaEvent.event_name, faturamento_handler_singleton.on_leitura_realizada)
    event_bus.subscribe(FaturaGeradaEvent.event_name, auditoria_handler_singleton.on_fatura_gerada)
    event_bus.subscribe(QualidadeInconformeEvent.event_name, auditoria_handler_singleton.on_qualidade_inconforme)
    _subscriptions_configured = True
_configure_subscriptions()

def get_usina_service() -> UsinaService:
    return usina_service_singleton

def get_central_geradora_service() -> CentralGeradoraService:
    return central_geradora_service_singleton

def get_subestacao_service() -> SubestacaoService:
    return subestacao_service_singleton

def get_linha_transmissao_service() -> LinhaTransmissaoService:
    return linha_transmissao_service_singleton

def get_geracao_service() -> GeracaoService:
    return geracao_service_singleton

def get_consumo_service() -> ConsumoService:
    return consumo_service_singleton

def get_faturamento_service() -> FaturamentoService:
    return faturamento_service_singleton

def get_outbox_worker() -> OutboxWorker:
    return outbox_worker_singleton
