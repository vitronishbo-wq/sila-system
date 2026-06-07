"""E2E fixtures partilhadas para os 5 testes de consolidação Educação."""

from __future__ import annotations

from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from apps.backend.app.modules.educacao.domain.models import CicloEnsino, Turma, Turno
from apps.backend.app.modules.educacao.domain.models.matricula import StatusMatricula
from apps.backend.app.modules.educacao.domain.models._workflow_record import WorkflowRecord
from apps.backend.app.modules.educacao.domain.wizard_session import WizardSession, WizardStatus
from apps.backend.app.modules.educacao.rbac.roles import RoleMinisterial as RoleEducacao
from sila_platform.governance.audit.logger import AuditLogger
from sila_platform.governance.digital_signature.engine import SignatureEngine
from sila_platform.governance.workflows.engine import WorkflowEngine


@pytest.fixture
def audit_logger():
    return AuditLogger()


@pytest.fixture
def signature_engine():
    return SignatureEngine()


@pytest.fixture
def workflow_engine():
    return WorkflowEngine()


@pytest.fixture
def citizen_id():
    return uuid4()


@pytest.fixture
def escola_id():
    return uuid4()


@pytest.fixture
def turma(escola_id):
    return Turma(
        id=uuid4(),
        escola_id=escola_id,
        ano_letivo_id=uuid4(),
        codigo="1A",
        classe="1a",
        turno=Turno.MANHA,
        capacidade=40,
        ativa=True,
    )


@pytest.fixture
def wizard_session(citizen_id):
    return WizardSession(
        id=uuid4(),
        citizen_id=citizen_id,
        status=WizardStatus.EM_CURSO,
        passo_atual=6,
        dados_estudante={
            "nome_completo": "João Silva",
            "data_nascimento": str(date.today() - timedelta(days=365 * 10)),
            "bi": "000000000AA000",
            "sexo": "M",
            "nacionalidade": "ANGOLANA",
        },
        selecao_escola={
            "escola_id": str(uuid4()),
            "turma_id": str(uuid4()),
            "ano_letivo_id": str(uuid4()),
            "classe": "1a",
            "turno": "MANHA",
        },
        pagamento={
            "modalidade": "referencia",
            "entidade": "12345",
            "referencia": "123456789",
            "valor": "2500.00",
            "moeda": "AOA",
            "status": "CONFIRMADO",
        },
        created_at=date.today(),
    )


@pytest.fixture
def mock_wizard_repo(wizard_session):
    repo = SimpleNamespace(
        get_by_id=AsyncMock(return_value=wizard_session),
        save=AsyncMock(side_effect=lambda s: s),
        get_active_by_citizen=AsyncMock(return_value=[wizard_session]),
    )
    return repo


@pytest.fixture
def mock_matricula_service(escola_id, turma):
    from apps.backend.app.modules.educacao.domain.models.matricula import Matricula

    matricula = Matricula(
        id=uuid4(),
        numero_processo="2026/E2E/0001",
        citizen_id=uuid4(),
        escola_id=escola_id,
        turma_id=turma.id,
        ano_letivo_id=turma.ano_letivo_id,
        data_matricula=date.today(),
        status=StatusMatricula.PENDENTE,
    )
    return SimpleNamespace(
        criar_matricula=AsyncMock(return_value=matricula),
    )


@pytest.fixture
def mock_event_bus():
    published = []

    class MockEventBus:
        async def publish(self, event):
            published.append(event)

        def get_published(self):
            return list(published)

        def clear(self):
            published.clear()

    bus = MockEventBus()
    return bus


@pytest.fixture
def mock_educacao_service_port():
    calls = []

    class MockPort:
        async def registrar_pagamento_propina(self, reference_id, payment_id, amount):
            calls.append({
                "reference_id": reference_id,
                "payment_id": payment_id,
                "amount": amount,
            })

        def get_calls(self):
            return list(calls)

    port = MockPort()
    return port
