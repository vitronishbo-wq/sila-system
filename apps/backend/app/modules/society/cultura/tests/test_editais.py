from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from apps.backend.app.modules.society.cultura.application.services.edital_service import (
    EditalService,
)
from apps.backend.app.modules.society.cultura.application.services.projeto_cultural_service import (
    ProjetoCulturalService,
)
from apps.backend.app.modules.society.cultura.domain.enums import (
    FaseEditalCultural,
    NaturezaProjetoCultural,
    StatusProjetoCultural,
    TipoEditalCultural,
    TipoProjetoCultural,
)
from apps.backend.app.modules.society.cultura.tests._fakes import (
    FakeRequestService,
    InMemoryEditalRepository,
    InMemoryProjetoCulturalRepository,
)


def test_publicar_edital_e_abrir_inscricoes() -> None:

    async def scenario() -> None:
        edital_repo = InMemoryEditalRepository()
        projeto_repo = InMemoryProjetoCulturalRepository()
        service = EditalService(
            edital_repo=edital_repo, projeto_repo=projeto_repo, request_service=FakeRequestService()
        )
        agora = datetime.utcnow()
        edital = await service.publicar_edital(
            numero="EDITAL-2026-001",
            titulo="Edital de Fomento 2026",
            tipo=TipoEditalCultural.FOMENTO,
            orgao_responsavel_id=uuid4(),
            valor_total=Decimal("100000.00"),
            data_publicacao=agora,
            data_inicio_inscricoes=agora,
            data_fim_inscricoes=agora + timedelta(days=30),
            vagas=10,
            descricao="Fomento a projetos culturais de base comunitaria.",
            criterios=["Relevancia cultural", "Impacto social"],
            documentos_necessarios=["BI", "Plano de trabalho"],
        )
        aberto = await service.abrir_inscricoes(edital.id)
        assert edital.numero == "EDITAL-2026-001"
        assert aberto.fase == FaseEditalCultural.INSCRICOES_ABERTAS

    asyncio.run(scenario())


def test_inscrever_e_selecionar_projetos() -> None:

    async def scenario() -> None:
        edital_repo = InMemoryEditalRepository()
        projeto_repo = InMemoryProjetoCulturalRepository()
        projeto_service = ProjetoCulturalService(projeto_repo=projeto_repo)
        edital_service = EditalService(edital_repo=edital_repo, projeto_repo=projeto_repo)
        agora = datetime.utcnow()
        edital = await edital_service.publicar_edital(
            numero="EDITAL-2026-002",
            titulo="Edital de Premios",
            tipo=TipoEditalCultural.PREMIO,
            orgao_responsavel_id=uuid4(),
            valor_total=Decimal("50000.00"),
            data_publicacao=agora,
            data_inicio_inscricoes=agora,
            data_fim_inscricoes=agora + timedelta(days=15),
            vagas=2,
            descricao="Premiacao de iniciativas culturais inovadoras.",
            criterios=["Inovacao"],
            documentos_necessarios=["Portfolio"],
        )
        await edital_service.abrir_inscricoes(edital.id)
        projeto = await projeto_service.cadastrar_projeto(
            titulo="Projeto Inovador",
            tipo=TipoProjetoCultural.DIFUSAO,
            natureza=NaturezaProjetoCultural.CULTURAL,
            proponente_cpf_cnpj="1122334455",
            proponente_nome="Coletivo Inovar",
            resumo="Projeto para difundir arte em bairros perifericos.",
            valor_solicitado=Decimal("20000.00"),
        )
        edital_inscrito = await edital_service.inscrever_projeto(
            edital_id=edital.id, projeto_id=projeto.id
        )
        edital_resultado = await edital_service.selecionar_projetos(
            edital_id=edital.id, projetos_ids=[projeto.id]
        )
        projeto_atualizado = await projeto_service.buscar_projeto(projeto.id)
        assert len(edital_inscrito.inscricoes) == 1
        assert edital_resultado.fase == FaseEditalCultural.RESULTADO_FINAL
        assert projeto_atualizado.status == StatusProjetoCultural.APROVADO

    asyncio.run(scenario())
