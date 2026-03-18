from __future__ import annotations
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID
from apps.backend.app.modules.logistics.domain.ports import BilhetagemRepositoryPort, ViagemRepositoryPort
from apps.backend.app.modules.logistics.domain.enums import StatusViagem
from apps.backend.app.modules.logistics.domain.models import DemandaOperacional, QualidadeServico

class OperacaoAnalyticsService:

    def __init__(self, *, viagem_repo: ViagemRepositoryPort, bilhetagem_repo: BilhetagemRepositoryPort | None=None) -> None:
        self._viagem_repo = viagem_repo
        self._bilhetagem_repo = bilhetagem_repo

    async def calcular_demanda(self, *, linha_id: UUID | None=None, data_inicio: datetime | None=None, data_fim: datetime | None=None) -> DemandaOperacional:
        viagens = await self._viagem_repo.list(linha_id=linha_id)
        viagens_filtradas = self._filtrar_periodo(viagens, data_inicio=data_inicio, data_fim=data_fim)
        total_viagens = len(viagens_filtradas)
        passageiros_total = 0
        for viagem in viagens_filtradas:
            passageiros_total += max(viagem.passageiros_embarcados or 0, 0)
        passageiros_media = (Decimal(passageiros_total) / Decimal(total_viagens) if total_viagens > 0 else Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        arrecadacao_total = Decimal('0.00')
        if self._bilhetagem_repo:
            eventos = await self._bilhetagem_repo.list(viagem_id=None, data_inicio=data_inicio, data_fim=data_fim)
            if linha_id:
                viagem_ids = {viagem.id for viagem in viagens_filtradas}
                eventos = [evento for evento in eventos if evento.viagem_id in viagem_ids]
            for evento in eventos:
                arrecadacao_total += evento.valor_pago
        return DemandaOperacional(viagens_total=total_viagens, passageiros_total=passageiros_total, passageiros_media_por_viagem=passageiros_media, arrecadacao_total=arrecadacao_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

    async def calcular_qualidade(self, *, linha_id: UUID | None=None, data_inicio: datetime | None=None, data_fim: datetime | None=None) -> QualidadeServico:
        viagens = await self._viagem_repo.list(linha_id=linha_id)
        viagens_filtradas = self._filtrar_periodo(viagens, data_inicio=data_inicio, data_fim=data_fim)
        total_viagens = len(viagens_filtradas)
        viagens_concluidas = 0
        viagens_canceladas = 0
        viagens_atrasadas = 0
        concluidas_no_prazo = 0
        for viagem in viagens_filtradas:
            if viagem.status == StatusViagem.CANCELADA:
                viagens_canceladas += 1
                continue
            is_atrasada = viagem.status == StatusViagem.ATRASADA
            if viagem.status == StatusViagem.CONCLUIDA and viagem.data_hora_chegada_real is not None and (viagem.data_hora_chegada_real > viagem.data_hora_chegada_prevista):
                is_atrasada = True
            if is_atrasada:
                viagens_atrasadas += 1
            if viagem.status == StatusViagem.CONCLUIDA:
                viagens_concluidas += 1
                if not is_atrasada:
                    concluidas_no_prazo += 1
        pontualidade = self._percentual(concluidas_no_prazo, viagens_concluidas)
        taxa_cancelamento = self._percentual(viagens_canceladas, total_viagens)
        taxa_atraso = self._percentual(viagens_atrasadas, total_viagens)
        return QualidadeServico(viagens_total=total_viagens, viagens_concluidas=viagens_concluidas, viagens_canceladas=viagens_canceladas, viagens_atrasadas=viagens_atrasadas, pontualidade_percentual=pontualidade, taxa_cancelamento_percentual=taxa_cancelamento, taxa_atraso_percentual=taxa_atraso)

    @staticmethod
    def _filtrar_periodo(viagens: list, *, data_inicio: datetime | None, data_fim: datetime | None) -> list:
        filtradas = viagens
        if data_inicio:
            filtradas = [viagem for viagem in filtradas if viagem.data_hora_saida >= data_inicio]
        if data_fim:
            filtradas = [viagem for viagem in filtradas if viagem.data_hora_saida <= data_fim]
        return filtradas

    @staticmethod
    def _percentual(numerador: int, denominador: int) -> Decimal:
        if denominador <= 0:
            return Decimal('0.00')
        return (Decimal(numerador) / Decimal(denominador) * Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)