from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta

import pytest

from apps.backend.app.modules.public_security.application.services.ocorrencia_service import (
    OcorrenciaService,
)
from apps.backend.app.modules.public_security.application.services.policial_service import (
    PolicialService,
)
from apps.backend.app.modules.public_security.application.services.unidade_policial_service import (
    UnidadePolicialService,
)
from apps.backend.app.modules.public_security.domain.enums import (
    PrioridadeOcorrencia,
    StatusOcorrencia,
    TipoAgente,
    TipoOcorrencia,
    TipoUnidadePolicial,
    TipoVinculo,
)
from apps.backend.app.modules.public_security.tests._fakes import (
    InMemoryOcorrenciaRepository,
    InMemoryPolicialRepository,
    InMemoryUnidadePolicialRepository,
)


def test_registrar_ocorrencia_sucesso() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(
            ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo
        )
        unidade = await unidade_service.cadastrar_unidade(
            nome="Delegacia Centro",
            tipo=TipoUnidadePolicial.DELEGACIA,
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua Centro",
            comandante="Delegado Centro",
        )
        policial = await policial_service.cadastrar_policial(
            unidade_id=unidade.id,
            nome="Rui Pereira",
            data_nascimento=date.today() - timedelta(days=365 * 34),
            cpf="111.222.333-44",
            rg="RG111222",
            tipo=TipoAgente.POLICIAL,
            vinculo=TipoVinculo.EFETIVO,
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            unidade_id=unidade.id,
            policial_responsavel_id=policial.id,
            tipo=TipoOcorrencia.ROUBO,
            prioridade=PrioridadeOcorrencia.ALTA,
            data_ocorrencia=datetime.now() - timedelta(hours=2),
            descricao="Roubo a estabelecimento comercial",
            municipio="Luanda",
            provincia="Luanda",
            vitimas=1,
            suspeitos=2,
        )
        assert ocorrencia.codigo_ocorrencia.startswith("OCO/")
        assert ocorrencia.status == StatusOcorrencia.REGISTRADA

    asyncio.run(scenario())


def test_registrar_ocorrencia_falha_policial_outra_unidade() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(
            ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo
        )
        unidade_a = await unidade_service.cadastrar_unidade(
            nome="Delegacia A",
            tipo=TipoUnidadePolicial.DELEGACIA,
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua A",
            comandante="Delegado A",
        )
        unidade_b = await unidade_service.cadastrar_unidade(
            nome="Delegacia B",
            tipo=TipoUnidadePolicial.DELEGACIA,
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua B",
            comandante="Delegado B",
        )
        policial_b = await policial_service.cadastrar_policial(
            unidade_id=unidade_b.id,
            nome="Paulo B",
            data_nascimento=date.today() - timedelta(days=365 * 32),
            cpf="555.666.777-88",
            rg="RG667788",
            tipo=TipoAgente.POLICIAL,
            vinculo=TipoVinculo.EFETIVO,
        )
        with pytest.raises(ValueError, match="nao pertence"):
            await ocorrencia_service.registrar_ocorrencia(
                unidade_id=unidade_a.id,
                policial_responsavel_id=policial_b.id,
                tipo=TipoOcorrencia.FURTO,
                prioridade=PrioridadeOcorrencia.MEDIA,
                data_ocorrencia=datetime.now() - timedelta(hours=1),
                descricao="Furto de veiculo",
                municipio="Luanda",
                provincia="Luanda",
            )

    asyncio.run(scenario())


def test_atualizar_status_ocorrencia() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(
            ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo
        )
        unidade = await unidade_service.cadastrar_unidade(
            nome="Posto C",
            tipo=TipoUnidadePolicial.POSTO_POLICIAL,
            municipio="Bengo",
            provincia="Bengo",
            endereco="Rua C",
            comandante="Comandante C",
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            unidade_id=unidade.id,
            tipo=TipoOcorrencia.AMEACA,
            prioridade=PrioridadeOcorrencia.BAIXA,
            data_ocorrencia=datetime.now() - timedelta(days=1),
            descricao="Ameaca verbal em via publica",
            municipio="Bengo",
            provincia="Bengo",
        )
        atualizada = await ocorrencia_service.atualizar_status(
            ocorrencia_id=ocorrencia.id,
            status=StatusOcorrencia.EM_ANDAMENTO,
            observacoes="Diligencia em curso",
        )
        assert atualizada.status == StatusOcorrencia.EM_ANDAMENTO
        assert atualizada.ativo is True

    asyncio.run(scenario())
