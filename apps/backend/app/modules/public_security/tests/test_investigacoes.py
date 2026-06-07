from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta

import pytest

from apps.backend.app.modules.public_security.application.services.investigacao_service import (
    InvestigacaoService,
)
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
    StatusInvestigacao,
    TipoAgente,
    TipoOcorrencia,
    TipoUnidadePolicial,
    TipoVinculo,
)
from apps.backend.app.modules.public_security.tests._fakes import (
    InMemoryInvestigacaoRepository,
    InMemoryOcorrenciaRepository,
    InMemoryPolicialRepository,
    InMemoryUnidadePolicialRepository,
)


def test_abrir_investigacao_sucesso() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        investigacao_repo = InMemoryInvestigacaoRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(
            ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo
        )
        investigacao_service = InvestigacaoService(
            investigacao_repo=investigacao_repo,
            ocorrencia_repo=ocorrencia_repo,
            policial_repo=policial_repo,
        )
        unidade = await unidade_service.cadastrar_unidade(
            nome="Delegacia Investigativa",
            tipo=TipoUnidadePolicial.DELEGACIA,
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua I",
            comandante="Delegado I",
        )
        delegado = await policial_service.cadastrar_policial(
            unidade_id=unidade.id,
            nome="Delegado Ramos",
            data_nascimento=date.today() - timedelta(days=365 * 40),
            cpf="111.444.777-00",
            rg="RG114477",
            tipo=TipoAgente.DELEGADO,
            vinculo=TipoVinculo.EFETIVO,
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            unidade_id=unidade.id,
            policial_responsavel_id=delegado.id,
            tipo=TipoOcorrencia.HOMICIDIO,
            prioridade=PrioridadeOcorrencia.CRITICA,
            data_ocorrencia=datetime.now() - timedelta(hours=6),
            descricao="Investigacao de homicidio consumado",
            municipio="Luanda",
            provincia="Luanda",
        )
        investigacao = await investigacao_service.abrir_investigacao(
            ocorrencia_id=ocorrencia.id,
            delegado_responsavel_id=delegado.id,
            resumo="Coleta inicial de evidencias",
        )
        assert investigacao.codigo_investigacao.startswith("INV/")
        assert investigacao.status == StatusInvestigacao.ABERTA

    asyncio.run(scenario())


def test_abrir_investigacao_falha_delegado_outra_unidade() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        investigacao_repo = InMemoryInvestigacaoRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(
            ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo
        )
        investigacao_service = InvestigacaoService(
            investigacao_repo=investigacao_repo,
            ocorrencia_repo=ocorrencia_repo,
            policial_repo=policial_repo,
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
        delegado_b = await policial_service.cadastrar_policial(
            unidade_id=unidade_b.id,
            nome="Delegado B",
            data_nascimento=date.today() - timedelta(days=365 * 37),
            cpf="222.333.444-55",
            rg="RG223344",
            tipo=TipoAgente.DELEGADO,
            vinculo=TipoVinculo.EFETIVO,
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            unidade_id=unidade_a.id,
            tipo=TipoOcorrencia.AMEACA,
            prioridade=PrioridadeOcorrencia.MEDIA,
            data_ocorrencia=datetime.now() - timedelta(hours=1),
            descricao="Ameaca em estabelecimento comercial",
            municipio="Luanda",
            provincia="Luanda",
        )
        with pytest.raises(ValueError, match="nao pertence"):
            await investigacao_service.abrir_investigacao(
                ocorrencia_id=ocorrencia.id, delegado_responsavel_id=delegado_b.id
            )

    asyncio.run(scenario())


def test_atualizar_status_investigacao() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        investigacao_repo = InMemoryInvestigacaoRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(
            ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo
        )
        investigacao_service = InvestigacaoService(
            investigacao_repo=investigacao_repo,
            ocorrencia_repo=ocorrencia_repo,
            policial_repo=policial_repo,
        )
        unidade = await unidade_service.cadastrar_unidade(
            nome="Posto Investigativo",
            tipo=TipoUnidadePolicial.POSTO_POLICIAL,
            municipio="Bengo",
            provincia="Bengo",
            endereco="Rua PI",
            comandante="Comandante PI",
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            unidade_id=unidade.id,
            tipo=TipoOcorrencia.DANO,
            prioridade=PrioridadeOcorrencia.BAIXA,
            data_ocorrencia=datetime.now() - timedelta(days=1),
            descricao="Dano ao patrimonio publico",
            municipio="Bengo",
            provincia="Bengo",
        )
        investigacao = await investigacao_service.abrir_investigacao(ocorrencia_id=ocorrencia.id)
        atualizada = await investigacao_service.atualizar_status(
            investigacao_id=investigacao.id,
            status=StatusInvestigacao.EM_ANDAMENTO,
            observacoes="Analise documental em curso",
        )
        assert atualizada.status == StatusInvestigacao.EM_ANDAMENTO
        assert atualizada.ativo is True

    asyncio.run(scenario())
