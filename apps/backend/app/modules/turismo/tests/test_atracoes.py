
from __future__ import annotations

import asyncio
from decimal import Decimal

from app.modules.turismo.application.services.atracao_service import AtracaoService
from app.modules.turismo.domain.enums import TipoAtracao
from app.modules.turismo.infrastructure.repositories.sqlalchemy_atracao_turistica_repository import (
    SQLAlchemyAtracaoTuristicaRepository,
)


def test_cadastrar_atracao_sucesso() -> None:
    repo = SQLAlchemyAtracaoTuristicaRepository()
    service = AtracaoService(repository=repo)

    result = asyncio.run(
        service.cadastrar(
            nome="Miradouro da Lua",
            tipo=TipoAtracao.NATURAL,
            descricao="Formacao geologica e paisagem natural.",
            endereco="Zona Costeira Sul",
            municipio="Belas",
            provincia="Luanda",
            horario_funcionamento="08:00-18:00",
            acessivel=False,
            gratuita=False,
            capacidade_visitantes_dia=300,
            valor_entrada=Decimal("2500"),
        )
    )

    assert result.codigo.startswith("AT/LUANDA/")
    assert result.tipo == TipoAtracao.NATURAL


def test_filtrar_atracoes_por_tipo_e_municipio() -> None:
    repo = SQLAlchemyAtracaoTuristicaRepository()
    service = AtracaoService(repository=repo)

    asyncio.run(
        service.cadastrar(
            nome="Fortaleza",
            tipo=TipoAtracao.HISTORICA,
            descricao="Patrimonio historico.",
            endereco="Centro",
            municipio="Luanda",
            provincia="Luanda",
            horario_funcionamento="09:00-17:00",
            acessivel=True,
        )
    )
    asyncio.run(
        service.cadastrar(
            nome="Praia Azul",
            tipo=TipoAtracao.NATURAL,
            descricao="Praia para lazer.",
            endereco="Litoral",
            municipio="Benguela",
            provincia="Benguela",
            horario_funcionamento="07:00-19:00",
            acessivel=True,
        )
    )

    filtradas = asyncio.run(service.listar(tipo=TipoAtracao.HISTORICA, municipio="Luanda"))
    assert len(filtradas) == 1
    assert filtradas[0].nome == "Fortaleza"
