
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock
from uuid import uuid4

from app.modules.turismo.application.services.agencia_viagens_service import AgenciaViagensService
from app.modules.turismo.infrastructure.repositories.sqlalchemy_agencia_viagens_repository import (
    SQLAlchemyAgenciaViagensRepository,
)


def test_cadastrar_agencia_viagens_sucesso() -> None:
    repo = SQLAlchemyAgenciaViagensRepository()
    citizen_service = AsyncMock()
    comercio_service = AsyncMock()
    request_service = AsyncMock()

    proprietario_id = uuid4()
    citizen_service.is_citizen_active.return_value = True
    comercio_service.agencia_cnpj_ativo.return_value = True

    service = AgenciaViagensService(
        repository=repo,
        citizen_service=citizen_service,
        comercio_service=comercio_service,
        request_service=request_service,
    )

    result = asyncio.run(
        service.cadastrar(
            nome_fantasia="Rota Angola",
            razao_social="Rota Angola Viagens Lda",
            cnpj="11.222.333/0001-44",
            email="contato@rotaangola.ao",
            telefone="222000123",
            endereco="Av. Principal",
            numero="101",
            bairro="Centro",
            municipio="Luanda",
            provincia="Luanda",
            cep="1000",
            proprietario_id=proprietario_id,
            especialidades=["ecoturismo", "roteiros culturais"],
        )
    )

    assert result.registro.startswith("AG/LUANDA/")
    assert result.nome_fantasia == "Rota Angola"
    request_service.create_request.assert_called_once()


def test_listar_agencias_filtra_por_municipio() -> None:
    repo = SQLAlchemyAgenciaViagensRepository()
    citizen_service = AsyncMock()
    citizen_service.is_citizen_active.return_value = True
    service = AgenciaViagensService(repository=repo, citizen_service=citizen_service)

    proprietario_id = uuid4()
    asyncio.run(
        service.cadastrar(
            nome_fantasia="Agencia Luanda",
            razao_social="Agencia Luanda SA",
            cnpj="10.000.000/0001-10",
            email="a@luanda.ao",
            telefone="2221",
            endereco="Rua A",
            numero="1",
            bairro="B1",
            municipio="Luanda",
            provincia="Luanda",
            cep="1000",
            proprietario_id=proprietario_id,
        )
    )
    asyncio.run(
        service.cadastrar(
            nome_fantasia="Agencia Benguela",
            razao_social="Agencia Benguela SA",
            cnpj="20.000.000/0001-20",
            email="a@benguela.ao",
            telefone="3331",
            endereco="Rua B",
            numero="2",
            bairro="B2",
            municipio="Benguela",
            provincia="Benguela",
            cep="2000",
            proprietario_id=proprietario_id,
        )
    )

    filtradas = asyncio.run(service.listar(municipio="Luanda"))
    assert len(filtradas) == 1
    assert filtradas[0].municipio == "Luanda"
