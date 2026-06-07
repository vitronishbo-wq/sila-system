from __future__ import annotations

from apps.backend.app.modules.resources.aguas_saneamento.application.bus import event_bus
from apps.backend.app.modules.resources.aguas_saneamento.application.events.fatura_events import (
    FaturaEmitidaEvent,
    FaturaPagamentoRegistradoEvent,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.handlers.financas_integration_handler import (
    FinancasIntegrationHandler,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.services.abastecimento_service import (
    AbastecimentoService,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.services.consumo_service import (
    ConsumoService,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.services.faturamento_service import (
    FaturamentoService,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.services.infraestrutura_service import (
    InfraestruturaService,
)
from apps.backend.app.modules.resources.aguas_saneamento.application.services.outorga_service import (
    OutorgaService,
)
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.adapters.financas_gateway import (
    FinancasGateway,
)
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.persistence.outbox import (
    SQLAlchemyOutboxRepository,
)
from apps.backend.app.modules.resources.aguas_saneamento.infrastructure.repositories import (
    SQLAlchemyAbastecimentoRepository,
    SQLAlchemyConsumoRepository,
    SQLAlchemyFaturaRepository,
    SQLAlchemyInfraestruturaRepository,
    SQLAlchemyOutorgaRepository,
)
from apps.backend.app.modules.resources.aguas_saneamento.workers.outbox_worker import OutboxWorker

outorga_repo_singleton = SQLAlchemyOutorgaRepository()
outorga_service_singleton = OutorgaService(outorga_repo=outorga_repo_singleton)
infraestrutura_repo_singleton = SQLAlchemyInfraestruturaRepository()
infraestrutura_service_singleton = InfraestruturaService(
    infraestrutura_repo=infraestrutura_repo_singleton
)
abastecimento_repo_singleton = SQLAlchemyAbastecimentoRepository()
abastecimento_service_singleton = AbastecimentoService(
    abastecimento_repo=abastecimento_repo_singleton
)
consumo_repo_singleton = SQLAlchemyConsumoRepository()
consumo_service_singleton = ConsumoService(consumo_repo=consumo_repo_singleton)
fatura_repo_singleton = SQLAlchemyFaturaRepository()
outbox_repo_singleton = SQLAlchemyOutboxRepository()
financas_gateway_singleton = FinancasGateway()
financas_integration_handler_singleton = FinancasIntegrationHandler(
    gateway=financas_gateway_singleton
)
event_bus.subscribe(
    FaturaEmitidaEvent.event_name, financas_integration_handler_singleton.on_fatura_emitida
)
event_bus.subscribe(
    FaturaPagamentoRegistradoEvent.event_name,
    financas_integration_handler_singleton.on_fatura_pagamento_registrado,
)
outbox_worker_singleton = OutboxWorker(outbox_repo=outbox_repo_singleton, event_bus=event_bus)
faturamento_service_singleton = FaturamentoService(
    fatura_repo=fatura_repo_singleton, outbox_repo=outbox_repo_singleton
)


def get_outorga_service() -> OutorgaService:
    return outorga_service_singleton


def get_infraestrutura_service() -> InfraestruturaService:
    return infraestrutura_service_singleton


def get_abastecimento_service() -> AbastecimentoService:
    return abastecimento_service_singleton


def get_consumo_service() -> ConsumoService:
    return consumo_service_singleton


def get_faturamento_service() -> FaturamentoService:
    return faturamento_service_singleton


def get_outbox_worker() -> OutboxWorker:
    return outbox_worker_singleton
