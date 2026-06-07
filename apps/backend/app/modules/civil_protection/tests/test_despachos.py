from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta

import pytest

from apps.backend.app.modules.civil_protection.application.services.bombeiro_service import (
    BombeiroService,
)
from apps.backend.app.modules.civil_protection.application.services.corporacao_service import (
    CorporacaoService,
)
from apps.backend.app.modules.civil_protection.application.services.despacho_service import (
    DespachoService,
)
from apps.backend.app.modules.civil_protection.application.services.ocorrencia_emergencial_service import (
    OcorrenciaEmergencialService,
)
from apps.backend.app.modules.civil_protection.domain.enums import (
    PrioridadeAtendimento,
    StatusDespacho,
    StatusOcorrenciaEmergencial,
    TipoOcorrenciaEmergencial,
)
from apps.backend.app.modules.civil_protection.tests._fakes import (
    InMemoryBombeiroRepository,
    InMemoryCorporacaoRepository,
    InMemoryDespachoRepository,
    InMemoryOcorrenciaEmergencialRepository,
)


def test_registrar_despacho_sucesso() -> None:

    async def scenario() -> None:
        corporacao_repo = InMemoryCorporacaoRepository()
        bombeiro_repo = InMemoryBombeiroRepository()
        ocorrencia_repo = InMemoryOcorrenciaEmergencialRepository()
        despacho_repo = InMemoryDespachoRepository()
        corporacao_service = CorporacaoService(corporacao_repo=corporacao_repo)
        bombeiro_service = BombeiroService(
            bombeiro_repo=bombeiro_repo, corporacao_repo=corporacao_repo
        )
        ocorrencia_service = OcorrenciaEmergencialService(
            ocorrencia_repo=ocorrencia_repo,
            corporacao_repo=corporacao_repo,
            bombeiro_repo=bombeiro_repo,
        )
        despacho_service = DespachoService(
            despacho_repo=despacho_repo,
            ocorrencia_repo=ocorrencia_repo,
            bombeiro_repo=bombeiro_repo,
        )
        corporacao = await corporacao_service.cadastrar_corporacao(
            nome="Corpo Despacho",
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua Despacho",
            comandante="Cmd Despacho",
        )
        bombeiro = await bombeiro_service.cadastrar_bombeiro(
            corporacao_id=corporacao.id,
            nome="Bombeiro D",
            data_nascimento=date.today() - timedelta(days=365 * 30),
            cpf="101.202.303-40",
            rg="RG101202",
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            corporacao_id=corporacao.id,
            bombeiro_responsavel_id=bombeiro.id,
            tipo=TipoOcorrenciaEmergencial.INCENDIO_URBANO,
            prioridade=PrioridadeAtendimento.ALTA,
            data_ocorrencia=datetime.now() - timedelta(hours=1),
            descricao="Incendio urbano em residencia",
            municipio="Luanda",
            provincia="Luanda",
        )
        despacho = await despacho_service.registrar_despacho(
            ocorrencia_id=ocorrencia.id,
            bombeiro_responsavel_id=bombeiro.id,
            meio_deslocamento="auto_bomba",
        )
        ocorrencia_atualizada = await ocorrencia_service.buscar_ocorrencia(ocorrencia.id)
        assert despacho.codigo_despacho.startswith("DSP/")
        assert despacho.status == StatusDespacho.GERADO
        assert ocorrencia_atualizada.status == StatusOcorrenciaEmergencial.EM_ATENDIMENTO

    asyncio.run(scenario())


def test_registrar_despacho_falha_bombeiro_outra_corporacao() -> None:

    async def scenario() -> None:
        corporacao_repo = InMemoryCorporacaoRepository()
        bombeiro_repo = InMemoryBombeiroRepository()
        ocorrencia_repo = InMemoryOcorrenciaEmergencialRepository()
        despacho_repo = InMemoryDespachoRepository()
        corporacao_service = CorporacaoService(corporacao_repo=corporacao_repo)
        bombeiro_service = BombeiroService(
            bombeiro_repo=bombeiro_repo, corporacao_repo=corporacao_repo
        )
        ocorrencia_service = OcorrenciaEmergencialService(
            ocorrencia_repo=ocorrencia_repo,
            corporacao_repo=corporacao_repo,
            bombeiro_repo=bombeiro_repo,
        )
        despacho_service = DespachoService(
            despacho_repo=despacho_repo,
            ocorrencia_repo=ocorrencia_repo,
            bombeiro_repo=bombeiro_repo,
        )
        corp_a = await corporacao_service.cadastrar_corporacao(
            nome="Corpo A",
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua A",
            comandante="Cmd A",
        )
        corp_b = await corporacao_service.cadastrar_corporacao(
            nome="Corpo B",
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua B",
            comandante="Cmd B",
        )
        bombeiro_b = await bombeiro_service.cadastrar_bombeiro(
            corporacao_id=corp_b.id,
            nome="Bombeiro B",
            data_nascimento=date.today() - timedelta(days=365 * 31),
            cpf="111.222.333-99",
            rg="RG778899",
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            corporacao_id=corp_a.id,
            tipo=TipoOcorrenciaEmergencial.DESABAMENTO,
            prioridade=PrioridadeAtendimento.MEDIA,
            data_ocorrencia=datetime.now() - timedelta(hours=1),
            descricao="Desabamento em edificio comercial",
            municipio="Luanda",
            provincia="Luanda",
        )
        with pytest.raises(ValueError, match="nao pertence"):
            await despacho_service.registrar_despacho(
                ocorrencia_id=ocorrencia.id, bombeiro_responsavel_id=bombeiro_b.id
            )

    asyncio.run(scenario())
