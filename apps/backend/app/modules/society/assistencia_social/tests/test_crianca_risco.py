from __future__ import annotations

import asyncio
from uuid import uuid4

from apps.backend.app.modules.society.assistencia_social.application.services.beneficiario_service import (
    BeneficiarioService,
)
from apps.backend.app.modules.society.assistencia_social.application.services.crianca_risco_service import (
    CriancaRiscoService,
)
from apps.backend.app.modules.society.assistencia_social.domain.enums import FaixaVulnerabilidade
from apps.backend.app.modules.society.assistencia_social.tests._fakes import (
    FakeCitizenService,
    FakeEducacaoService,
    FakeRequestService,
    InMemoryBeneficiarioRepo,
    InMemoryCadastroUnicoRepo,
    InMemoryCriancaRiscoRepo,
)


def test_crianca_risco_dispara_solicitacao_quando_fora_da_escola() -> None:

    async def scenario() -> None:
        beneficiario_repo = InMemoryBeneficiarioRepo()
        request = FakeRequestService()
        beneficiario_service = BeneficiarioService(
            beneficiario_repo=beneficiario_repo,
            citizen_service=FakeCitizenService(active=True),
            cadastro_unico_repo=InMemoryCadastroUnicoRepo(),
            request_service=request,
        )
        beneficiario = await beneficiario_service.cadastrar_beneficiario(
            citizen_id=uuid4(), faixa_vulnerabilidade=FaixaVulnerabilidade.ALTA
        )
        service = CriancaRiscoService(
            crianca_repo=InMemoryCriancaRiscoRepo(),
            beneficiario_repo=beneficiario_repo,
            educacao_service=FakeEducacaoService(estudantes_ativos=set()),
            request_service=request,
        )
        registro = await service.registrar_crianca_risco(
            beneficiario_id=beneficiario.id,
            citizen_id_crianca=uuid4(),
            idade=12,
            motivo="risco de evasao",
            escolarizada=True,
        )
        assert registro.escolarizada is False
        assert any(
            call["request_type"] == "ASSISTENCIA_CRIANCA_FORA_ESCOLA" for call in request.calls
        )
        erro = None
        try:
            await service.registrar_crianca_risco(
                beneficiario_id=beneficiario.id,
                citizen_id_crianca=uuid4(),
                idade=18,
                motivo="fora da faixa",
                escolarizada=False,
            )
        except ValueError as exc:
            erro = str(exc)
        assert erro is not None
        assert "0 e 17" in erro

    asyncio.run(scenario())
