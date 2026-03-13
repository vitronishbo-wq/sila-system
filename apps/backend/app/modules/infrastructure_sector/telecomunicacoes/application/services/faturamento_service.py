from __future__ import annotations
from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID
from app.modules.infrastructure_sector.telecomunicacoes.application.events.definitions import FaturaTelecomGeradaEvent
from app.modules.infrastructure_sector.telecomunicacoes.application.ports.assinante_repository_port import AssinanteRepositoryPort
from app.modules.infrastructure_sector.telecomunicacoes.application.ports.fatura_repository_port import FaturaRepositoryPort
from app.modules.infrastructure_sector.telecomunicacoes.application.ports.outbox_repository_port import OutboxRepositoryPort
from app.modules.infrastructure_sector.telecomunicacoes.domain.models.fatura_telecom import FaturaTelecom
from app.modules.infrastructure_sector.telecomunicacoes.domain.models.franquia import Franquia

class FaturamentoService:

    def __init__(self, *, assinante_repo: AssinanteRepositoryPort, fatura_repo: FaturaRepositoryPort, outbox_repo: OutboxRepositoryPort | None=None) -> None:
        self._assinante_repo = assinante_repo
        self._fatura_repo = fatura_repo
        self._outbox_repo = outbox_repo

    async def gerar_fatura_mensal(self, assinante_id: UUID, referencia: str, *, consumo_total_gb: Decimal) -> FaturaTelecom:
        assinante = await self._assinante_repo.get_by_id(assinante_id)
        if assinante is None:
            raise ValueError('Assinante nao encontrado')
        if not assinante.ativo:
            raise ValueError('Assinante inativo')
        franquia = Franquia.padrao()
        valor_plano = Decimal(str(assinante.valor_mensal if assinante.valor_mensal is not None else 0.0))
        valor_excedente = franquia.calcular_valor_excedente(consumo_total_gb)
        fatura = FaturaTelecom.gerar(assinante_id=assinante.id, referencia=referencia, consumo_total_gb=consumo_total_gb, franquia_gb=franquia.franquia_gb, valor_plano=valor_plano, valor_excedente=valor_excedente, data_vencimento=date.today() + timedelta(days=10))
        fatura.numero_fatura = await self._fatura_repo.next_numero()
        saved = await self._fatura_repo.save(fatura)
        if self._outbox_repo is not None:
            await self._outbox_repo.enqueue(FaturaTelecomGeradaEvent.from_fatura(saved))
        return saved

    async def listar_faturas_assinante(self, assinante_id: UUID) -> list[FaturaTelecom]:
        return await self._fatura_repo.list_by_assinante(assinante_id)

    async def buscar_por_numero(self, numero_fatura: str) -> FaturaTelecom:
        item = await self._fatura_repo.get_by_numero(numero_fatura)
        if item is None:
            raise ValueError('Fatura nao encontrada')
        return item