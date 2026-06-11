#!/usr/bin/env python3
import asyncio
import os
from datetime import date
from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from apps.backend.app.core.db import Base, register_models
from apps.backend.app.core.bridges.identity_bridge import CitizenFUC
from apps.backend.app.core.identity import IdentityContext
from apps.backend.app.modules.governance.workflow.api.router import router as workflow_router
from apps.backend.app.modules.governance.workflow.infrastructure.repositories.workflow_repository import (
    WorkflowRepository,
)
from apps.backend.app.modules.governance.workflow.domain.models.workflow_definition import WorkflowDefinition
from apps.backend.app.modules.governance.workflow.domain.models.workflow_state import WorkflowState
from apps.backend.app.modules.governance.workflow.domain.models.workflow_transition import WorkflowTransition
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_definition_model import (
    WorkflowDefinitionModel,
)
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_history_model import (
    WorkflowHistoryModel,
)
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_instance_model import (
    WorkflowInstanceModel,
)
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_state_model import (
    WorkflowStateModel,
)
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_task_model import (
    WorkflowTaskModel,
)
from apps.backend.app.modules.governance.workflow.infrastructure.models.workflow_transition_model import (
    WorkflowTransitionModel,
)


def _database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        from apps.backend.app.core.settings import settings

        url = str(settings.DATABASE_URL or "")
    if not url:
        raise RuntimeError("DATABASE_URL is required")
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


async def main():
    register_models()
    registry = getattr(Base, "registry", None)
    if registry is not None and hasattr(registry, "configure"):
        registry.configure()

    engine = create_async_engine(_database_url(), echo=False, pool_pre_ping=True, poolclass=NullPool)

    required_tables = [
        CitizenFUC.__table__,
        WorkflowDefinitionModel.__table__,
        WorkflowStateModel.__table__,
        WorkflowTransitionModel.__table__,
        WorkflowInstanceModel.__table__,
        WorkflowTaskModel.__table__,
        WorkflowHistoryModel.__table__,
    ]
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync_conn: Base.metadata.create_all(sync_conn, tables=required_tables, checkfirst=True))

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False)

    user_id = uuid4()
    citizen_id = uuid4()

    # seed citizen
    async with session_factory() as session:
        session.add(
            CitizenFUC(
                citizen_id=citizen_id,
                full_name="Cidadao Workflow",
                birth_date=date(1998, 5, 1),
                gender="M",
                is_active=True,
                document_number=f"BI-{citizen_id.hex[:12]}",
                vital_status="alive",
            )
        )
        await session.commit()

    # create workflow definition
    async with session_factory() as session:
        repo = WorkflowRepository(session)
        code = f"WF_DEBUG_{uuid4().hex[:6]}"
        definition = WorkflowDefinition(code=code, name=f"Workflow {code}", entity_type="SERVICE_REQUEST")
        start_state = WorkflowState(workflow_id=definition.id, code="INICIO", name="Inicio", is_initial=True)
        end_state = WorkflowState(workflow_id=definition.id, code="FIM", name="Fim", is_final=True)
        await repo.save_definition(definition)
        await repo.save_state(start_state)
        await repo.save_state(end_state)
        transition = WorkflowTransition(
            workflow_id=definition.id,
            from_state_id=start_state.id,
            to_state_id=end_state.id,
            code="AVANCAR",
            name="Avancar",
            condition_expression="identidade.validar_cidadao_ativo",
            post_actions={
                "call_adapter": {
                    "adapter": "identidade",
                    "method": "validar_cidadao_ativo",
                    "args": {"citizen_id": "$citizen_id"},
                    "save_as": "cidadao_ativo",
                }
            },
        )
        await repo.save_transition(transition)
        await repo.commit()

    # build app
    app = FastAPI()
    app.include_router(workflow_router, prefix="/api/v1")

    async def _override_get_db():
        async with session_factory() as session:
            yield session

    async def _override_identity_context():
        return IdentityContext({
            "user_id": str(user_id),
            "citizen_id": str(citizen_id),
            "email": "workflow-debug@sila.local",
        })

    from apps.backend.app.api.deps import get_db, get_identity_context
    app.dependency_overrides[get_db] = _override_get_db
    app.dependency_overrides[get_identity_context] = _override_identity_context

    with TestClient(app) as client:
        start_response = client.post(
            "/api/v1/workflow/start",
            json={
                "workflow_code": definition.code,
                "entity_type": "SERVICE_REQUEST",
                "entity_id": str(uuid4()),
                "variables": {},
            },
        )
        print("start status", start_response.status_code)
        print(start_response.text)
        instance_id = start_response.json().get("id")
        trans = client.post(f"/api/v1/workflow/instances/{instance_id}/transitions", json={"transition_code": "AVANCAR", "form_data": {}})
        print("transition status", trans.status_code)
        print(trans.text)


if __name__ == "__main__":
    asyncio.run(main())
