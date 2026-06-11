from __future__ import annotations

from uuid import uuid4

import pytest

from apps.backend.app.modules.educacao.application.canonical.wizard_matricula_service import (
    WizardMatriculaService,
)
from apps.backend.app.modules.educacao.domain.wizard_session import WizardStatus


@pytest.mark.asyncio
async def test_wizard_cancel_publishes_event(wizard_session, mock_wizard_repo, mock_event_bus):
    svc = WizardMatriculaService(
        wizard_repo=mock_wizard_repo,
        matricula_service=None,
        session=None,
        pagamento_service=None,
        event_bus=mock_event_bus,
    )

    result = await svc.cancelar(wizard_session.id)
    assert result.status == WizardStatus.CANCELADO

    published = mock_event_bus.get_published()
    cancelled = [e for e in published if e.event_type == "WizardCancelled"]
    assert len(cancelled) == 1
    evt = cancelled[0]
    assert getattr(evt, "correlation_id", None) == wizard_session.id
