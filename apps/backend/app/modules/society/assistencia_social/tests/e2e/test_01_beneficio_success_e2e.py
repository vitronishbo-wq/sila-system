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
from apps.backend.app.processes.contracts import BeneficioAprovadoEvent


class MockPublisher:
    def __init__(self):
        self.published = []
        self.appended = []

    async def publish_atomic(self, event, **kwargs):
        self.published.append((event, kwargs))
        # simulate event store append
        self.appended.append((event, kwargs))
        return event


@pytest.mark.asyncio
async def test_beneficio_success_e2e() -> None:
    beneficio_repo = InMemoryBeneficioRepo()
    beneficiario_repo = InMemoryBeneficiarioRepo()
    programa_repo = InMemoryProgramaRepo()
    pcd_repo = InMemoryPCDRepo()
    saude = FakeSaudeService(cobertura=True)
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

    beneficiario = Beneficiario.cadastrar(numero_registro="R-1", citizen_id=uuid4(), cadastro_unico_id=None, faixa_vulnerabilidade=FaixaVulnerabilidade.BAIXA)
    await beneficiario_repo.save(beneficiario)

    # submit using the saved beneficiary id
    beneficio = await handlers.submit(beneficiario_id=beneficiario.id, tipo=TipoBeneficio.BOLSA_FAMILIA, valor=Decimal("100.00"))

    # advance workflow to verificacao_nif (admin actor)
    wf.avancar(str(beneficio.id), actor="admin")
    await handlers.verify_nif(beneficio.id, valid=True, nif="123456789")
    # advance workflow to verificacao_ss (admin actor)
    wf.avancar(str(beneficio.id), actor="admin")
    await handlers.verify_ss(beneficio.id, valid=True, ss_number="SS123")

    # advance to aprovado and finalize
    wf.avancar(str(beneficio.id), actor="system")
    await handlers.approve(beneficio.id, valor=100.0)

    # assertions
    assert any(evt[0].event_type == "BeneficioAprovadoEvent" for evt in publisher.appended)
    # correlation_id set on process events stored as domain events payloads
    approved = [e for e, _ in publisher.appended if e.event_type == "BeneficioAprovadoEvent"]
    assert approved, "BeneficioAprovadoEvent should be published"
    assert all(e.correlation_id == beneficio.id for e in approved)
