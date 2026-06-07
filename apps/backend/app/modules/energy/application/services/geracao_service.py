from __future__ import annotations

import asyncio
import logging
from time import perf_counter
from typing import Any

from apps.backend.app.modules.energy.application.ports import (
    CentralGeradoraRepositoryPort,
    LinhaTransmissaoRepositoryPort,
    SubestacaoRepositoryPort,
)

logger = logging.getLogger(__name__)


class GeracaoService:
    def __init__(
        self,
        *,
        central_repo: CentralGeradoraRepositoryPort,
        sub_repo: SubestacaoRepositoryPort,
        linha_repo: LinhaTransmissaoRepositoryPort,
        repo_timeout_seconds: float = 1.0,
        slow_log_threshold_seconds: float = 0.5,
    ) -> None:
        self._central_repo = central_repo
        self._sub_repo = sub_repo
        self._linha_repo = linha_repo
        self._repo_timeout_seconds = repo_timeout_seconds
        self._slow_log_threshold_seconds = slow_log_threshold_seconds

    async def get_visao_consolidada(self) -> dict[str, Any]:
        started = perf_counter()
        centrais, erro_centrais = await self._safe_fetch("centrais", self._central_repo.list_all)
        subestacoes, erro_subestacoes = await self._safe_fetch(
            "subestacoes", self._sub_repo.list_all
        )
        linhas, erro_linhas = await self._safe_fetch("linhas", self._linha_repo.list_all)
        erros: dict[str, str] = {}
        if erro_centrais:
            erros["centrais"] = erro_centrais
        if erro_subestacoes:
            erros["subestacoes"] = erro_subestacoes
        if erro_linhas:
            erros["linhas"] = erro_linhas
        elapsed = perf_counter() - started
        if elapsed > self._slow_log_threshold_seconds:
            logger.warning(
                "Dashboard de geracao lento",
                extra={
                    "elapsed_seconds": round(elapsed, 4),
                    "repo_timeout_seconds": self._repo_timeout_seconds,
                    "degraded": bool(erros),
                },
            )
        return {
            "centrais": centrais,
            "subestacoes": subestacoes,
            "linhas": linhas,
            "errors": erros,
            "degraded": bool(erros),
        }

    async def _safe_fetch(self, nome: str, callback) -> tuple[list[Any], str | None]:
        try:
            values = await asyncio.wait_for(callback(), timeout=self._repo_timeout_seconds)
            return (values, None)
        except TimeoutError:
            logger.error(
                "Timeout ao consultar repositorio de energia",
                extra={"repo": nome, "timeout_seconds": self._repo_timeout_seconds},
            )
            return ([], f"timeout ao consultar {nome}")
        except Exception as exc:
            logger.exception("Falha ao consultar repositorio de energia", extra={"repo": nome})
            return ([], f"falha ao consultar {nome}: {exc}")
