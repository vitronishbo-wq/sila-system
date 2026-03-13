from __future__ import annotations

from datetime import date
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select

from app.api.deps import get_current_user
from app.core.db import AsyncSessionLocal, Base, engine
from app.modules.educacao.api.router import router as educacao_router
from app.modules.governance.service_requests.api.router import router as service_requests_router
from app.modules.educacao.infrastructure.models import (
    AnoLetivoModel,
    EscolaModel,
    MatriculaModel,
    TurmaModel,
)
from app.core.bridges.identity_bridge import CitizenFUC
from app.modules.governance.service_requests.infrastructure.models.service_request_model import (
    ServiceRequestModel,
)
from app.modules.governance.service_requests.infrastructure.models.attachment_model import AttachmentModel
from app.modules.governance.service_requests.infrastructure.models.request_event_model import RequestEventModel


@pytest.mark.asyncio
async def test_fluxo_completo_matricula():
    test_app = FastAPI()
    test_app.include_router(educacao_router, prefix="/api/v1")
    test_app.include_router(service_requests_router, prefix="/api/v1")

    citizen_id = UUID("123e4567-e89b-12d3-a456-426614174000")
    escola_id = UUID("123e4567-e89b-12d3-a456-426614174001")
    turma_id = UUID("123e4567-e89b-12d3-a456-426614174002")
    ano_letivo_id = UUID("123e4567-e89b-12d3-a456-426614174003")
    codigo_med = f"LUA/KAZ/{uuid4().hex[:8].upper()}"

    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: Base.metadata.create_all(
                bind=sync_conn,
                tables=[
                    CitizenFUC.__table__,
                    EscolaModel.__table__,
                    TurmaModel.__table__,
                    AnoLetivoModel.__table__,
                    MatriculaModel.__table__,
                    ServiceRequestModel.__table__,
                    AttachmentModel.__table__,
                    RequestEventModel.__table__,
                ],
            )
        )

    async with AsyncSessionLocal() as session:
        # Limpeza ampla para garantir unicidade de request_number entre execuções.
        await session.execute(delete(AttachmentModel))
        await session.execute(delete(RequestEventModel))
        await session.execute(delete(ServiceRequestModel))
        await session.execute(delete(MatriculaModel).where(MatriculaModel.citizen_id == citizen_id))
        await session.execute(delete(TurmaModel).where(TurmaModel.id == turma_id))
        await session.execute(delete(EscolaModel).where(EscolaModel.id == escola_id))
        await session.execute(delete(AnoLetivoModel).where(AnoLetivoModel.id == ano_letivo_id))
        await session.execute(delete(CitizenFUC).where(CitizenFUC.citizen_id == citizen_id))

        session.add(
            CitizenFUC(
                citizen_id=citizen_id,
                full_name="Antonio Manuel da Silva",
                document_number="003456789LA042",
                birth_date=date(2012, 1, 1),
                email="antonio.silva@test.ao",
                vital_status="alive",
                is_active=True,
            )
        )
        session.add(
            EscolaModel(
                id=escola_id,
                codigo_med=codigo_med,
                nome="Escola Primaria 1o de Maio",
                tipo="publica",
                ciclos=["primario"],
                provincia="Luanda",
                municipio="Cazenga",
                comuna="Hoji-ya-Henda",
                bairro="11 de Novembro",
                endereco="Rua Principal",
                ativa=True,
            )
        )
        session.add(
            TurmaModel(
                id=turma_id,
                escola_id=escola_id,
                ano_letivo_id=ano_letivo_id,
                codigo="5A",
                classe="5a",
                turno="manha",
                capacidade=45,
                ativa=True,
            )
        )
        session.add(
            AnoLetivoModel(
                id=ano_letivo_id,
                ano=date.today().year,
                data_inicio=date(date.today().year, 9, 1),
                data_fim=date(date.today().year + 1, 6, 30),
                ativo=True,
            )
        )
        await session.commit()

    async def _fake_current_user():
        return {
            "email": "truman@gmail.com",
            "user_id": str(citizen_id),
            "roles": ["CITIZEN"],
            "system": "IAM",
        }

    test_app.dependency_overrides[get_current_user] = _fake_current_user
    try:
        async with AsyncClient(
            transport=ASGITransport(app=test_app),
            base_url="http://testserver",
        ) as client:
            create_payload = {
                "citizen_id": str(citizen_id),
                "escola_id": str(escola_id),
                "turma_id": str(turma_id),
                "ano_letivo_id": str(ano_letivo_id),
                "observacoes": "Teste E2E Educacao",
            }

            response = await client.post("/api/v1/educacao/matriculas/", json=create_payload)
            assert response.status_code == 201, response.text
            created = response.json()
            matricula_id = created["id"]
            assert created["status"] == "pendente"
            assert created["numero_processo"].startswith(f"{date.today().year}/")

            response = await client.post(
                f"/api/v1/educacao/matriculas/{matricula_id}/ativar",
                json={"confirmacao_documental": True},
            )
            assert response.status_code == 200, response.text
            activated = response.json()
            assert activated["status"] == "ativa"

            response = await client.get(f"/api/v1/educacao/matriculas/citizen/{citizen_id}")
            assert response.status_code == 200, response.text
            rows = response.json()
            assert any(item["id"] == matricula_id for item in rows)

            response = await client.post("/api/v1/educacao/matriculas/", json=create_payload)
            assert response.status_code == 409, response.text

            response = await client.get(f"/api/v1/service-requests/entity/{matricula_id}")
            assert response.status_code == 200, response.text
            tracking = response.json()
            assert len(tracking) >= 1
            assert any(item["type"] == "education_enrollment" for item in tracking)
            assert any(item["status"] == "completed" for item in tracking)
    finally:
        test_app.dependency_overrides.pop(get_current_user, None)

    async with AsyncSessionLocal() as session:
        req_stmt = select(ServiceRequestModel).where(
            ServiceRequestModel.citizen_id == citizen_id,
        )
        records = (await session.execute(req_stmt)).scalars().all()
        assert records, "Nenhum tracking request foi persistido no nucleo"
