from __future__ import annotations

import asyncio

from apps.backend.app.modules.society.cultura.application.services.espaco_cultural_service import (
    EspacoCulturalService,
)
from apps.backend.app.modules.society.cultura.domain.enums import TipoEspacoCultural
from apps.backend.app.modules.society.cultura.tests._fakes import (
    FakeRequestService,
    InMemoryEspacoCulturalRepository,
)


def test_cadastrar_espaco_cultural_sucesso() -> None:

    async def scenario() -> None:
        service = EspacoCulturalService(
            espaco_repo=InMemoryEspacoCulturalRepository(), request_service=FakeRequestService()
        )
        espaco = await service.cadastrar_espaco(
            nome="Museu Nacional",
            tipo=TipoEspacoCultural.MUSEU,
            municipio="Luanda",
            provincia="Luanda",
            endereco="Av. 4 de Fevereiro",
            capacidade=300,
            area_m2=1200.0,
            administracao="PUBLICA",
            responsavel_cpf="123456789",
            acessibilidade=True,
        )
        assert espaco.codigo_espaco.startswith("ESP/")
        assert espaco.nome == "Museu Nacional"
        assert espaco.acessibilidade is True

    asyncio.run(scenario())


def test_listar_espacos_por_tipo() -> None:

    async def scenario() -> None:
        service = EspacoCulturalService(espaco_repo=InMemoryEspacoCulturalRepository())
        await service.cadastrar_espaco(
            nome="Teatro A",
            tipo=TipoEspacoCultural.TEATRO,
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua A",
            capacidade=200,
            area_m2=700,
            administracao="PUBLICA",
            responsavel_cpf="123",
        )
        await service.cadastrar_espaco(
            nome="Museu B",
            tipo=TipoEspacoCultural.MUSEU,
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua B",
            capacidade=100,
            area_m2=400,
            administracao="PRIVADA",
            responsavel_cpf="456",
        )
        teatros = await service.listar_espacos(tipo=TipoEspacoCultural.TEATRO)
        assert len(teatros) == 1
        assert teatros[0].nome == "Teatro A"

    asyncio.run(scenario())
