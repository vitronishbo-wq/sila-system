from __future__ import annotations

import asyncio
from datetime import date
from uuid import uuid4

import pytest

from apps.backend.app.modules.society.juventude.application.services.programa_service import (
    ProgramaService,
)
from apps.backend.app.modules.society.juventude.domain.enums import StatusPrograma, TipoPrograma
from apps.backend.app.modules.society.juventude.tests._fakes import InMemoryProgramaRepository


def test_criar_programa_sucesso() -> None:

    async def scenario() -> None:
        service = ProgramaService(programa_repo=InMemoryProgramaRepository())
        result = await service.criar_programa(
            nome="Programa Primeiro Emprego",
            tipo=TipoPrograma.PRIMEIRO_EMPREGO,
            data_inicio=date.today(),
            vagas=120,
            municipio="Luanda",
            provincia="Luanda",
        )
        assert result.codigo_programa.startswith("PRG/")
        assert result.status == StatusPrograma.PLANEADO

    asyncio.run(scenario())


def test_atualizar_status_programa() -> None:

    async def scenario() -> None:
        service = ProgramaService(programa_repo=InMemoryProgramaRepository())
        programa = await service.criar_programa(
            nome="Programa Lideranca Jovem", tipo=TipoPrograma.LIDERANCA, data_inicio=date.today()
        )
        atualizado = await service.atualizar_status(
            programa_id=programa.id, status=StatusPrograma.ATIVO
        )
        assert atualizado.status == StatusPrograma.ATIVO

    asyncio.run(scenario())


def test_buscar_programa_inexistente() -> None:

    async def scenario() -> None:
        service = ProgramaService(programa_repo=InMemoryProgramaRepository())
        with pytest.raises(ValueError, match="Programa"):
            await service.buscar_programa(programa_id=uuid4())

    asyncio.run(scenario())
