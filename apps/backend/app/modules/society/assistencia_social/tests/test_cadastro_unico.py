from __future__ import annotations

import asyncio
from decimal import Decimal
from uuid import uuid4

from apps.backend.app.modules.society.assistencia_social.application.services.cadastro_unico_service import (
    CadastroUnicoService,
)
from apps.backend.app.modules.society.assistencia_social.tests._fakes import (
    FakeCitizenService,
    FakeEducacaoService,
    FakeJuventudeService,
    FakeRequestService,
    InMemoryCadastroUnicoRepo,
)


def test_cadastro_unico_dispara_alertas_e_programas() -> None:

    async def scenario() -> None:
        crianca = uuid4()
        jovem_risco = uuid4()
        responsavel = uuid4()
        service = CadastroUnicoService(
            cadastro_repo=InMemoryCadastroUnicoRepo(),
            citizen_service=FakeCitizenService(active=True),
            educacao_service=FakeEducacaoService(estudantes_ativos=set()),
            juventude_service=FakeJuventudeService(jovens_em_risco={jovem_risco}),
            request_service=FakeRequestService(),
        )
        cadastro, programas, alertas = await service.registrar_cadastro(
            citizen_id_responsavel=responsavel,
            renda_per_capita=Decimal("80.00"),
            composicao_familiar=[
                {"citizen_id": str(crianca), "idade": 10},
                {"citizen_id": str(jovem_risco), "idade": 19},
                {"idade": 67},
            ],
            condicoes_moradia="ALUGADA",
            acesso_agua=True,
            acesso_energia=True,
        )
        assert cadastro.codigo.startswith("CAD/")
        assert "BOLSA_FAMILIA" in programas
        assert "BPC_IDOSO" in programas
        assert any("CRIANCA_FORA_ESCOLA" in a for a in alertas)
        assert any("JOVEM_EM_RISCO_SOCIAL" in a for a in alertas)

    asyncio.run(scenario())
