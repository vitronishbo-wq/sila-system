from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta
from uuid import uuid4

import pytest

from apps.backend.app.modules.public_security.application.services.cadeia_custodia_service import (
    CadeiaCustodiaService,
)
from apps.backend.app.modules.public_security.application.services.ocorrencia_service import (
    OcorrenciaService,
)
from apps.backend.app.modules.public_security.application.services.policial_service import (
    PolicialService,
)
from apps.backend.app.modules.public_security.application.services.prova_pericial_service import (
    ProvaPericialService,
)
from apps.backend.app.modules.public_security.application.services.unidade_policial_service import (
    UnidadePolicialService,
)
from apps.backend.app.modules.public_security.application.services.vestigio_service import (
    VestigioService,
)
from apps.backend.app.modules.public_security.domain.enums import (
    PrioridadeOcorrencia,
    StatusVestigio,
    TipoAgente,
    TipoOcorrencia,
    TipoProva,
    TipoUnidadePolicial,
    TipoVestigio,
    TipoVinculo,
)
from apps.backend.app.modules.public_security.tests._fakes import (
    InMemoryCadeiaCustodiaRepository,
    InMemoryOcorrenciaRepository,
    InMemoryPolicialRepository,
    InMemoryProvaPericialRepository,
    InMemoryUnidadePolicialRepository,
    InMemoryVestigioRepository,
)


def test_registrar_vestigio_sucesso() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        cadeia_repo = InMemoryCadeiaCustodiaRepository()
        vestigio_repo = InMemoryVestigioRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(
            ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo
        )
        prova_service = ProvaPericialService(
            prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo
        )
        cadeia_service = CadeiaCustodiaService(
            cadeia_repo=cadeia_repo, prova_repo=prova_repo, policial_repo=policial_repo
        )
        vestigio_service = VestigioService(
            vestigio_repo=vestigio_repo, cadeia_repo=cadeia_repo, policial_repo=policial_repo
        )
        unidade = await unidade_service.cadastrar_unidade(
            nome="Laboratorio Vestigios",
            tipo=TipoUnidadePolicial.BASE_OPERACIONAL,
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua V1",
            comandante="Comandante V1",
        )
        coletor = await policial_service.cadastrar_policial(
            unidade_id=unidade.id,
            nome="Coletor Vestigio",
            data_nascimento=date.today() - timedelta(days=365 * 34),
            cpf="101.202.303-44",
            rg="RG101202",
            tipo=TipoAgente.POLICIAL,
            vinculo=TipoVinculo.EFETIVO,
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            unidade_id=unidade.id,
            policial_responsavel_id=coletor.id,
            tipo=TipoOcorrencia.ROUBO,
            prioridade=PrioridadeOcorrencia.ALTA,
            data_ocorrencia=datetime.now() - timedelta(hours=2),
            descricao="Ocorrencia para coleta de vestigio",
            municipio="Luanda",
            provincia="Luanda",
        )
        prova = await prova_service.coletar_prova(
            ocorrencia_id=ocorrencia.id,
            tipo=TipoProva.MATERIAL,
            descricao="Prova material para cadeia",
            local_coleta="Local A",
            coletado_por_id=coletor.id,
        )
        cadeia = await cadeia_service.iniciar_cadeia(
            prova_id=prova.id, local_atual="Cofre A", responsavel_id=coletor.id
        )
        vestigio = await vestigio_service.registrar_vestigio(
            cadeia_custodia_id=cadeia.id,
            tipo=TipoVestigio.OBJETO,
            descricao="Objeto encontrado no local da ocorrencia",
            localizacao="Sala principal",
            coletado_por_id=coletor.id,
        )
        assert vestigio.codigo_vestigio.startswith("VST/")
        assert vestigio.status == StatusVestigio.COLETADO

    asyncio.run(scenario())


def test_registrar_vestigio_falha_cadeia_inexistente() -> None:

    async def scenario() -> None:
        service = VestigioService(
            vestigio_repo=InMemoryVestigioRepository(),
            cadeia_repo=InMemoryCadeiaCustodiaRepository(),
            policial_repo=InMemoryPolicialRepository(),
        )
        with pytest.raises(ValueError, match="Cadeia de custodia nao encontrada"):
            await service.registrar_vestigio(
                cadeia_custodia_id=uuid4(),
                tipo=TipoVestigio.DOCUMENTO,
                descricao="Documento com vestigio",
                localizacao="Arquivo",
            )

    asyncio.run(scenario())


def test_atualizar_status_vestigio() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        cadeia_repo = InMemoryCadeiaCustodiaRepository()
        vestigio_repo = InMemoryVestigioRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(
            ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo
        )
        prova_service = ProvaPericialService(
            prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo
        )
        cadeia_service = CadeiaCustodiaService(
            cadeia_repo=cadeia_repo, prova_repo=prova_repo, policial_repo=policial_repo
        )
        vestigio_service = VestigioService(
            vestigio_repo=vestigio_repo, cadeia_repo=cadeia_repo, policial_repo=policial_repo
        )
        unidade = await unidade_service.cadastrar_unidade(
            nome="Laboratorio Vestigios B",
            tipo=TipoUnidadePolicial.BASE_OPERACIONAL,
            municipio="Bengo",
            provincia="Bengo",
            endereco="Rua V2",
            comandante="Comandante V2",
        )
        coletor = await policial_service.cadastrar_policial(
            unidade_id=unidade.id,
            nome="Operador V2",
            data_nascimento=date.today() - timedelta(days=365 * 32),
            cpf="909.808.707-66",
            rg="RG908070",
            tipo=TipoAgente.POLICIAL,
            vinculo=TipoVinculo.EFETIVO,
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            unidade_id=unidade.id,
            policial_responsavel_id=coletor.id,
            tipo=TipoOcorrencia.DANO,
            prioridade=PrioridadeOcorrencia.MEDIA,
            data_ocorrencia=datetime.now() - timedelta(days=1),
            descricao="Ocorrencia para update de vestigio",
            municipio="Bengo",
            provincia="Bengo",
        )
        prova = await prova_service.coletar_prova(
            ocorrencia_id=ocorrencia.id,
            tipo=TipoProva.DIGITAL,
            descricao="Midia para preservacao",
            local_coleta="Sala B",
        )
        cadeia = await cadeia_service.iniciar_cadeia(
            prova_id=prova.id, local_atual="Cofre B", responsavel_id=coletor.id
        )
        vestigio = await vestigio_service.registrar_vestigio(
            cadeia_custodia_id=cadeia.id,
            tipo=TipoVestigio.MIDIA_DIGITAL,
            descricao="Pen drive apreendido",
            localizacao="Mesa 3",
        )
        atualizado = await vestigio_service.atualizar_status(
            vestigio_id=vestigio.id,
            status=StatusVestigio.PRESERVADO,
            observacoes="Preservado em embalagem lacrada",
        )
        assert atualizado.status == StatusVestigio.PRESERVADO
        assert atualizado.ativo is True

    asyncio.run(scenario())
