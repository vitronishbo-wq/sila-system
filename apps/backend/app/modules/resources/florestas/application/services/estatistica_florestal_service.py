from __future__ import annotations

import asyncio
from typing import Any

from apps.backend.app.modules.resources.florestas.application.ports.agricultura_service_port import (
    AgriculturaServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.ambiente_service_port import (
    AmbienteServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.comercio_externo_service_port import (
    ComercioExternoServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.concessionario_florestal_repository_port import (
    ConcessionarioFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.energia_service_port import (
    EnergiaServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.geosampa_service_port import (
    GeosampaServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.gestao_fundiaria_service_port import (
    GestaoFundiariaServicePort,
)
from apps.backend.app.modules.resources.florestas.application.ports.inventario_florestal_repository_port import (
    InventarioFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.plano_manejo_florestal_repository_port import (
    PlanoManejoFlorestalRepositoryPort,
)
from apps.backend.app.modules.resources.florestas.application.ports.unidade_manejo_repository_port import (
    UnidadeManejoRepositoryPort,
)


class EstatisticaFlorestalService:
    def __init__(
        self,
        *,
        operador_repo: ConcessionarioFlorestalRepositoryPort,
        unidade_repo: UnidadeManejoRepositoryPort,
        plano_repo: PlanoManejoFlorestalRepositoryPort,
        inventario_repo: InventarioFlorestalRepositoryPort,
        ambiente_service: AmbienteServicePort,
        gestao_fundiaria_service: GestaoFundiariaServicePort,
        agricultura_service: AgriculturaServicePort,
        energia_service: EnergiaServicePort,
        comercio_externo_service: ComercioExternoServicePort,
        geosampa_service: GeosampaServicePort,
    ):
        self._operador_repo = operador_repo
        self._unidade_repo = unidade_repo
        self._plano_repo = plano_repo
        self._inventario_repo = inventario_repo
        self._integracoes: dict[str, Any] = {
            "ambiente": ambiente_service,
            "gestao_fundiaria": gestao_fundiaria_service,
            "agricultura": agricultura_service,
            "energia": energia_service,
            "comercio_externo": comercio_externo_service,
            "geosampa": geosampa_service,
        }

    async def gerar_resumo_operacional(self) -> dict[str, Any]:
        operadores = await self._operador_repo.list_all()
        total_operadores = len(operadores)
        total_unidades = 0
        total_planos = 0
        total_inventarios = 0
        for operador in operadores:
            unidades = await self._unidade_repo.list_by_operador(operador.id)
            total_unidades += len(unidades)
            for unidade in unidades:
                total_planos += len(await self._plano_repo.list_by_unidade(unidade.id))
                total_inventarios += len(await self._inventario_repo.list_by_unidade(unidade.id))
        return {
            "total_operadores": total_operadores,
            "total_unidades_manejo": total_unidades,
            "total_planos_manejo": total_planos,
            "total_inventarios": total_inventarios,
            "media_unidades_por_operador": round(total_unidades / total_operadores, 2)
            if total_operadores
            else 0.0,
            "media_planos_por_unidade": round(total_planos / total_unidades, 2)
            if total_unidades
            else 0.0,
        }

    async def gerar_status_integracao(self) -> dict[str, Any]:
        items = await asyncio.gather(
            *[self._coletar_status_modulo(nome, porta) for nome, porta in self._integracoes.items()]
        )
        total = len(items)
        ativos = sum(1 for item in items if item["available"])
        return {
            "integracao_ok": ativos == total,
            "modulos_ativos": ativos,
            "modulos_totais": total,
            "modulos": items,
        }

    async def gerar_dashboard(self) -> dict[str, Any]:
        operacional, integracao = await asyncio.gather(
            self.gerar_resumo_operacional(), self.gerar_status_integracao()
        )
        return {"operacional": operacional, "integracao": integracao}

    async def _coletar_status_modulo(self, nome: str, porta: Any) -> dict[str, Any]:
        available = await self._safe_bool(porta, "available")
        payload = await self._safe_payload(porta, "integration_payload")
        return {"modulo": nome, "available": available, "detalhes": payload}

    @staticmethod
    async def _safe_bool(obj: Any, method_name: str) -> bool:
        method = getattr(obj, method_name, None)
        if not callable(method):
            return False
        try:
            value = method()
            if asyncio.iscoroutine(value):
                value = await value
            return bool(value)
        except Exception:
            return False

    @staticmethod
    async def _safe_payload(obj: Any, method_name: str) -> dict[str, Any]:
        method = getattr(obj, method_name, None)
        if not callable(method):
            return {}
        try:
            value = method()
            if asyncio.iscoroutine(value):
                value = await value
            return value if isinstance(value, dict) else {}
        except Exception:
            return {}
