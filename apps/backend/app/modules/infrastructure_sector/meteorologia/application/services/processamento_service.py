from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from apps.backend.app.modules.infrastructure_sector.meteorologia.application.ports import (
    AlertaServicePort,
    EstacaoRepositoryPort,
    ObservacaoRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.meteorologia.domain.models import (
    ObservacaoMeteorologica,
)


class ProcessamentoService:
    def __init__(
        self,
        *,
        observacao_repository: ObservacaoRepositoryPort,
        estacao_repository: EstacaoRepositoryPort,
        alerta_service: AlertaServicePort | None = None,
    ) -> None:
        self.observacao_repository = observacao_repository
        self.estacao_repository = estacao_repository
        self.alerta_service = alerta_service

    async def processar_observacao(self, observacao: ObservacaoMeteorologica) -> dict[str, Any]:
        resultado: dict[str, Any] = {
            "sucesso": False,
            "observacao_id": str(observacao.id),
            "alertas_gerados": 0,
            "warnings": [],
            "erros": [],
            "observacao": None,
        }
        resultado["warnings"] = observacao.validar_dados()
        estacao = None
        if observacao.estacao_id:
            estacao = await self.estacao_repository.get_by_id(observacao.estacao_id)
            if estacao is None:
                resultado["erros"].append(f"Estacao {observacao.estacao_id} nao encontrada")
                return resultado
            if not estacao.is_active:
                resultado["warnings"].append(
                    f"Estacao {estacao.codigo} esta {estacao.status.value}"
                )
        alertas = observacao.analisar_severidade()
        resultado["alertas_gerados"] = len(alertas)
        try:
            persisted = await self.observacao_repository.save(observacao)
            resultado["sucesso"] = True
            resultado["observacao"] = persisted
        except Exception as exc:
            resultado["erros"].append(f"Erro ao persistir observacao: {exc}")
            return resultado
        if alertas and self.alerta_service and observacao.estacao_id:
            for alerta in alertas:
                publicado = await self.alerta_service.publicar_alerta(
                    estacao_id=observacao.estacao_id, alerta=alerta, observacao_id=observacao.id
                )
                if not publicado:
                    tipo_alerta = alerta.get("tipo", "DESCONHECIDO")
                    resultado["warnings"].append(f"Falha ao publicar alerta {tipo_alerta}")
            if estacao and estacao.provincia:
                severos = [
                    alerta for alerta in alertas if alerta.get("severidade") in {"HIGH", "EXTREME"}
                ]
                if severos:
                    ok = await self.alerta_service.notificar_defesa_civil(
                        alertas=severos, provincia=estacao.provincia
                    )
                    if not ok:
                        resultado["warnings"].append("Falha ao notificar Defesa Civil")
        return resultado

    async def processar_lote_observacoes(
        self, observacoes: list[ObservacaoMeteorologica]
    ) -> dict[str, Any]:
        resultados: list[dict[str, Any]] = []
        total_alertas = 0
        sucessos = 0
        falhas = 0
        for observacao in observacoes:
            resultado = await self.processar_observacao(observacao)
            resultados.append(resultado)
            if resultado["sucesso"]:
                sucessos += 1
                total_alertas += int(resultado["alertas_gerados"])
            else:
                falhas += 1
        return {
            "total": len(observacoes),
            "sucessos": sucessos,
            "falhas": falhas,
            "total_alertas": total_alertas,
            "detalhes": resultados,
        }

    async def obter_observacao(self, observacao_id: UUID) -> ObservacaoMeteorologica:
        observacao = await self.observacao_repository.get_by_id(observacao_id)
        if observacao is None:
            raise ValueError("Observacao nao encontrada")
        return observacao

    async def listar_observacoes_estacao(
        self,
        *,
        estacao_id: UUID,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 100,
    ) -> list[ObservacaoMeteorologica]:
        return await self.observacao_repository.list_by_estacao(
            estacao_id=estacao_id, start_date=start_date, end_date=end_date, limit=limit
        )

    async def listar_observacoes_com_alertas(
        self,
        *,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int = 50,
    ) -> list[ObservacaoMeteorologica]:
        return await self.observacao_repository.list_with_alerts(
            start_date=start_date, end_date=end_date, limit=limit
        )
