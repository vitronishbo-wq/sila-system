import asyncio
from decimal import Decimal
from uuid import uuid4

import pytest

from apps.backend.app.modules.society.assistencia_social.tests._fakes import (
    InMemoryBeneficioRepo,
    InMemoryBeneficiarioRepo,
    InMemoryProgramaRepo,
    FakeSaudeService,
    FakeEmpregoService,
    FakeRequestService,
)

from apps.backend.app.modules.society.assistencia_social.application.services.beneficio_service import (
    BeneficioService,
)
from apps.backend.app.modules.society.assistencia_social.domain.models import Beneficiario
from apps.backend.app.modules.society.assistencia_social.domain.enums import TipoBeneficio, FaixaVulnerabilidade
from apps.backend.app.modules.society.assistencia_social.tests._fakes import InMemoryPCDRepo
from apps.backend.app.modules.society.assistencia_social.workflows.beneficio_workflow import BeneficioWorkflowEngine
from apps.backend.app.modules.society.assistencia_social.handlers import BeneficioHandlers


class MockPublisher:
    def __init__(self):
        self.published = []
        self.appended = []

    async def publish_atomic(self, event, **kwargs):
        self.published.append((event, kwargs))
        self.appended.append((event, kwargs))
        return event


@pytest.mark.asyncio
async def test_beneficio_reject_e2e() -> None:
    beneficio_repo = InMemoryBeneficioRepo()
    beneficiario_repo = InMemoryBeneficiarioRepo()
    programa_repo = InMemoryProgramaRepo()
    pcd_repo = InMemoryPCDRepo()
    saude = FakeSaudeService(cobertura=False)
    emprego = FakeEmpregoService()
    request_svc = FakeRequestService()

    svc = BeneficioService(
        beneficio_repo=beneficio_repo,
        beneficiario_repo=beneficiario_repo,
        programa_repo=programa_repo,
        pcd_repo=pcd_repo,
        saude_service=saude,
        emprego_service=emprego,
        request_service=request_svc,
    )

    wf = BeneficioWorkflowEngine()
    publisher = MockPublisher()
    handlers = BeneficioHandlers(beneficio_service=svc, beneficio_repo=beneficio_repo, workflow_engine=wf, event_publisher=publisher)

    beneficiario = Beneficiario.cadastrar(numero_registro="R-2", citizen_id=uuid4(), cadastro_unico_id=None, faixa_vulnerabilidade=FaixaVulnerabilidade.BAIXA)
    await beneficiario_repo.save(beneficiario)

    # submit
    beneficio = await handlers.submit(beneficiario_id=beneficiario.id, tipo=TipoBeneficio.BOLSA_FAMILIA, valor=Decimal("50.00"))

    # advance workflow to verificacao_nif (admin actor)
    wf.avancar(str(beneficio.id), actor="admin")
    # NIF valid
    await handlers.verify_nif(beneficio.id, valid=True, nif="123456789")

    # advance workflow to verificacao_ss (admin actor)
    wf.avancar(str(beneficio.id), actor="admin")
    # SS invalid triggers rejection
    await handlers.verify_ss(beneficio.id, valid=False, ss_number=None)

    # ensure the beneficio in repo is NEGADO
    b = await beneficio_repo.get_by_id(beneficio.id)
    assert b is not None
    assert b.status.name.lower() == "negado"
