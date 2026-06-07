from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta

from apps.backend.app.modules.civil_protection.application.services.atendimento_service import (
    AtendimentoService,
)
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
    StatusAtendimento,
    StatusDespacho,
    StatusOcorrenciaEmergencial,
    TipoOcorrenciaEmergencial,
)
from apps.backend.app.modules.civil_protection.tests._fakes import (
    InMemoryAtendimentoRepository,
    InMemoryBombeiroRepository,
    InMemoryCorporacaoRepository,
    InMemoryDespachoRepository,
    InMemoryOcorrenciaEmergencialRepository,
)


def test_registrar_atendimento_conclui_despacho() -> None:

    async def scenario() -> None:
        corporacao_repo = InMemoryCorporacaoRepository()
        bombeiro_repo = InMemoryBombeiroRepository()
        ocorrencia_repo = InMemoryOcorrenciaEmergencialRepository()
        despacho_repo = InMemoryDespachoRepository()
        atendimento_repo = InMemoryAtendimentoRepository()
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
        atendimento_service = AtendimentoService(
            atendimento_repo=atendimento_repo,
            despacho_repo=despacho_repo,
            ocorrencia_repo=ocorrencia_repo,
            bombeiro_repo=bombeiro_repo,
        )
        corporacao = await corporacao_service.cadastrar_corporacao(
            nome="Corpo Atendimento",
            municipio="Luanda",
            provincia="Luanda",
            endereco="Rua Atendimento",
            comandante="Cmd Atendimento",
        )
        bombeiro = await bombeiro_service.cadastrar_bombeiro(
            corporacao_id=corporacao.id,
            nome="Bombeiro A",
            data_nascimento=date.today() - timedelta(days=365 * 30),
            cpf="201.202.203-40",
            rg="RG201202",
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            corporacao_id=corporacao.id,
            bombeiro_responsavel_id=bombeiro.id,
            tipo=TipoOcorrenciaEmergencial.INUNDACAO,
            prioridade=PrioridadeAtendimento.ALTA,
            data_ocorrencia=datetime.now() - timedelta(hours=1),
            descricao="Inundacao com familias desalojadas",
            municipio="Luanda",
            provincia="Luanda",
        )
        despacho = await despacho_service.registrar_despacho(
            ocorrencia_id=ocorrencia.id, bombeiro_responsavel_id=bombeiro.id
        )
        atendimento = await atendimento_service.registrar_atendimento(
            despacho_id=despacho.id,
            local_atendimento="Bairro Azul",
            vitimas_atendidas=3,
            desalojados_atendidos=5,
            equipe_responsavel_id=bombeiro.id,
        )
        despacho_atualizado = await despacho_service.buscar_despacho(despacho.id)
        assert atendimento.codigo_atendimento.startswith("ATE/")
        assert atendimento.status == StatusAtendimento.INICIADO
        assert despacho_atualizado.status == StatusDespacho.CONCLUIDO

    asyncio.run(scenario())


def test_finalizar_atendimento_conclui_ocorrencia() -> None:

    async def scenario() -> None:
        corporacao_repo = InMemoryCorporacaoRepository()
        bombeiro_repo = InMemoryBombeiroRepository()
        ocorrencia_repo = InMemoryOcorrenciaEmergencialRepository()
        despacho_repo = InMemoryDespachoRepository()
        atendimento_repo = InMemoryAtendimentoRepository()
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
        atendimento_service = AtendimentoService(
            atendimento_repo=atendimento_repo,
            despacho_repo=despacho_repo,
            ocorrencia_repo=ocorrencia_repo,
            bombeiro_repo=bombeiro_repo,
        )
        corporacao = await corporacao_service.cadastrar_corporacao(
            nome="Corpo Finalizacao",
            municipio="Bengo",
            provincia="Bengo",
            endereco="Rua Final",
            comandante="Cmd Final",
        )
        bombeiro = await bombeiro_service.cadastrar_bombeiro(
            corporacao_id=corporacao.id,
            nome="Bombeiro F",
            data_nascimento=date.today() - timedelta(days=365 * 33),
            cpf="301.302.303-44",
            rg="RG301302",
        )
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(
            corporacao_id=corporacao.id,
            bombeiro_responsavel_id=bombeiro.id,
            tipo=TipoOcorrenciaEmergencial.DESLIZAMENTO,
            prioridade=PrioridadeAtendimento.ALTA,
            data_ocorrencia=datetime.now() - timedelta(hours=2),
            descricao="Deslizamento em encosta residencial",
            municipio="Bengo",
            provincia="Bengo",
        )
        despacho = await despacho_service.registrar_despacho(
            ocorrencia_id=ocorrencia.id, bombeiro_responsavel_id=bombeiro.id
        )
        atendimento = await atendimento_service.registrar_atendimento(
            despacho_id=despacho.id,
            local_atendimento="Encosta Sul",
            equipe_responsavel_id=bombeiro.id,
        )
        finalizado = await atendimento_service.finalizar_atendimento(
            atendimento_id=atendimento.id, resumo="Atendimento concluido sem novos riscos"
        )
        ocorrencia_atualizada = await ocorrencia_service.buscar_ocorrencia(ocorrencia.id)
        assert finalizado.status == StatusAtendimento.FINALIZADO
        assert finalizado.fim_atendimento is not None
        assert ocorrencia_atualizada.status == StatusOcorrenciaEmergencial.CONCLUIDA

    asyncio.run(scenario())
