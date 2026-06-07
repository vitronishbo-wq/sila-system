from __future__ import annotations

from collections import defaultdict
from datetime import date
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from apps.backend.app.modules.society.emprego.api.deps import (
    get_candidato_service,
    get_certificacao_service,
    get_concurso_service,
    get_formacao_service,
    get_mediacao_service,
    get_oferta_service,
    get_trabalho_service,
)
from apps.backend.app.modules.society.emprego.api.router import router as emprego_router
from apps.backend.app.modules.society.emprego.application.ports import (
    CandidatoRepositoryPort,
    CitizenServicePort,
    RequestServicePort,
    WorkflowRepositoryPort,
)
from apps.backend.app.modules.society.emprego.application.services import (
    CandidatoService,
    CertificacaoService,
    ConcursoService,
    FormacaoService,
    MediacaoService,
    OfertaService,
    TrabalhoService,
)
from apps.backend.app.modules.society.emprego.domain.enums import (
    Escolaridade,
    SituacaoProfissional,
    StatusCandidato,
    WorkflowStatus,
)
from apps.backend.app.modules.society.emprego.domain.models._workflow_record import (
    WorkflowEmpregoRecord,
)
from apps.backend.app.modules.society.emprego.domain.models.candidato import Candidato


class InMemoryCitizenService(CitizenServicePort):
    def __init__(self, active_citizens: set[UUID]):
        self.active_citizens = set(active_citizens)

    async def get_citizen(self, citizen_id: UUID):
        if citizen_id in self.active_citizens:
            return SimpleNamespace(id=citizen_id, is_active=True)
        return None

    async def is_citizen_active(self, citizen_id: UUID) -> bool:
        return citizen_id in self.active_citizens


class InMemoryRequestService(RequestServicePort):
    def __init__(self):
        self.created: list[dict] = []
        self.completed: list[dict] = []

    async def create_request(
        self,
        *,
        request_type: str,
        entity_id: UUID,
        citizen_id: UUID,
        numero_processo: str,
        metadata: dict | None = None,
    ):
        self.created.append(
            {
                "request_type": request_type,
                "entity_id": entity_id,
                "citizen_id": citizen_id,
                "numero_processo": numero_processo,
                "metadata": metadata or {},
            }
        )
        return uuid4()

    async def complete_request(
        self, *, entity_id: UUID, actor_id: UUID, metadata: dict | None = None
    ) -> bool:
        self.completed.append(
            {"entity_id": entity_id, "actor_id": actor_id, "metadata": metadata or {}}
        )
        return True


class InMemoryCandidatoRepository(CandidatoRepositoryPort):
    def __init__(self):
        self.by_id: dict[UUID, Candidato] = {}
        self.by_citizen: dict[UUID, Candidato] = {}
        self.seq_by_year: dict[int, int] = defaultdict(int)

    async def save(self, candidato: Candidato) -> Candidato:
        self.by_id[candidato.id] = candidato
        self.by_citizen[candidato.citizen_id] = candidato
        return candidato

    async def get_by_id(self, id: UUID):
        return self.by_id.get(id)

    async def get_by_citizen(self, citizen_id: UUID):
        return self.by_citizen.get(citizen_id)

    async def list_by_filtros(
        self, escolaridade=None, situacao=None, area_interesse=None, ativos=True
    ):
        data = list(self.by_id.values())
        if escolaridade is not None:
            data = [c for c in data if c.escolaridade == escolaridade]
        if situacao is not None:
            data = [c for c in data if c.situacao == situacao]
        if area_interesse is not None:
            data = [c for c in data if area_interesse in c.areas_interesse]
        if ativos:
            data = [c for c in data if c.status == StatusCandidato.ATIVO]
        return data

    async def next_numero_processo(self, ano: int) -> str:
        self.seq_by_year[ano] += 1
        return f"CAND/{ano}/{self.seq_by_year[ano]:04d}"


class InMemoryWorkflowRepository(WorkflowRepositoryPort):
    def __init__(self):
        self.by_id: dict[UUID, WorkflowEmpregoRecord] = {}
        self.seq_by_prefix_year: dict[tuple[str, int], int] = defaultdict(int)

    async def save(self, item: WorkflowEmpregoRecord) -> WorkflowEmpregoRecord:
        self.by_id[item.id] = item
        return item

    async def get_by_id(self, item_id: UUID):
        return self.by_id.get(item_id)

    async def list_by_citizen(self, citizen_id: UUID, service_type: str | None = None):
        data = [item for item in self.by_id.values() if item.citizen_id == citizen_id]
        if service_type is not None:
            data = [item for item in data if item.service_type == service_type]
        return sorted(data, key=lambda it: it.data_registro, reverse=True)

    async def exists_active_for_citizen(self, citizen_id: UUID, service_type: str) -> bool:
        active = {WorkflowStatus.PENDENTE, WorkflowStatus.EM_ANALISE, WorkflowStatus.APROVADA}
        return any(
            item.citizen_id == citizen_id
            and item.service_type == service_type
            and (item.status in active)
            for item in self.by_id.values()
        )

    async def next_numero_processo(self, ano: int, prefix: str) -> str:
        key = (prefix, ano)
        self.seq_by_prefix_year[key] += 1
        return f"{prefix}/{ano}/{self.seq_by_prefix_year[key]:04d}"


@pytest.fixture
def e2e_client():
    citizens = {
        "candidato": uuid4(),
        "oferta": uuid4(),
        "mediacao": uuid4(),
        "formacao": uuid4(),
        "trabalho": uuid4(),
        "concurso": uuid4(),
        "certificacao": uuid4(),
    }
    citizen_service = InMemoryCitizenService(set(citizens.values()))
    request_service = InMemoryRequestService()
    candidato_repo = InMemoryCandidatoRepository()
    workflow_repo = InMemoryWorkflowRepository()
    candidato_service = CandidatoService(
        candidato_repo=candidato_repo, citizen_repo=citizen_service, request_service=request_service
    )
    oferta_service = OfertaService(
        repository=workflow_repo, citizen_service=citizen_service, request_service=request_service
    )
    mediacao_service = MediacaoService(
        repository=workflow_repo, citizen_service=citizen_service, request_service=request_service
    )
    formacao_service = FormacaoService(
        repository=workflow_repo, citizen_service=citizen_service, request_service=request_service
    )
    trabalho_service = TrabalhoService(
        repository=workflow_repo, citizen_service=citizen_service, request_service=request_service
    )
    concurso_service = ConcursoService(
        repository=workflow_repo, citizen_service=citizen_service, request_service=request_service
    )
    certificacao_service = CertificacaoService(
        repository=workflow_repo, citizen_service=citizen_service, request_service=request_service
    )
    app = FastAPI()
    app.include_router(emprego_router)
    app.dependency_overrides[get_candidato_service] = lambda: candidato_service
    app.dependency_overrides[get_oferta_service] = lambda: oferta_service
    app.dependency_overrides[get_mediacao_service] = lambda: mediacao_service
    app.dependency_overrides[get_formacao_service] = lambda: formacao_service
    app.dependency_overrides[get_trabalho_service] = lambda: trabalho_service
    app.dependency_overrides[get_concurso_service] = lambda: concurso_service
    app.dependency_overrides[get_certificacao_service] = lambda: certificacao_service
    with TestClient(app) as client:
        yield (client, citizens, request_service)


@pytest.mark.integration
def test_e2e_candidatos_fluxo_completo(e2e_client):
    client, citizens, request_service = e2e_client
    citizen_id = citizens["candidato"]
    created = client.post(
        "/emprego/candidatos/",
        json={
            "citizen_id": str(citizen_id),
            "escolaridade": Escolaridade.SECUNDARIA.value,
            "situacao": SituacaoProfissional.DESEMPREGADO.value,
            "areas_interesse": ["administracao", "vendas"],
        },
    )
    assert created.status_code == 201
    created_payload = created.json()
    candidato_id = created_payload["id"]
    assert created_payload["numero_processo"].startswith(f"CAND/{date.today().year}/")
    assert created_payload["status"] == StatusCandidato.ATIVO.value
    found = client.get(f"/emprego/candidatos/{candidato_id}")
    assert found.status_code == 200
    assert found.json()["citizen_id"] == str(citizen_id)
    listed = client.get(
        "/emprego/candidatos", params={"situacao": SituacaoProfissional.DESEMPREGADO.value}
    )
    assert listed.status_code == 200
    assert any(item["id"] == candidato_id for item in listed.json())
    deactivated = client.post(
        f"/emprego/candidatos/{candidato_id}/desativar",
        json={"actor_id": str(uuid4()), "motivo": "Encerramento voluntario"},
    )
    assert deactivated.status_code == 200
    assert deactivated.json()["status"] == StatusCandidato.INATIVO.value
    assert deactivated.json()["observacoes"] == "Encerramento voluntario"
    assert len(request_service.created) >= 1
    assert len(request_service.completed) >= 1


@pytest.mark.integration
def test_e2e_ofertas_fluxo_criar_consultar_concluir(e2e_client):
    client, citizens, _ = e2e_client
    citizen_id = citizens["oferta"]
    created = client.post(
        "/emprego/ofertas",
        json={
            "citizen_id": str(citizen_id),
            "observacoes": "Oferta de emprego",
            "metadata": {"setor": "servicos"},
        },
    )
    assert created.status_code == 201
    created_payload = created.json()
    item_id = created_payload["id"]
    assert created_payload["numero_processo"].startswith(f"OFER/{date.today().year}/")
    assert created_payload["service_type"] == "oferta_emprego"
    found = client.get(f"/emprego/workflow/{item_id}")
    assert found.status_code == 200
    assert found.json()["id"] == item_id
    concluded = client.post(
        f"/emprego/workflow/{item_id}/concluir",
        json={"actor_id": str(uuid4()), "observacoes": "Processo concluido"},
    )
    assert concluded.status_code == 200
    assert concluded.json()["status"] == WorkflowStatus.CONCLUIDA.value
    by_citizen = client.get(f"/emprego/workflow/citizen/{citizen_id}")
    assert by_citizen.status_code == 200
    assert any(item["id"] == item_id for item in by_citizen.json())


@pytest.mark.integration
def test_e2e_fluxo_criacao_por_dominios_workflow(e2e_client):
    client, citizens, _ = e2e_client
    cases = [
        ("/emprego/mediacoes", citizens["mediacao"], "mediacao", "MEDI"),
        ("/emprego/formacoes/profissional", citizens["formacao"], "formacao_profissional", "FORM"),
        ("/emprego/trabalho/reclamacoes", citizens["trabalho"], "reclamacao_trabalhista", "TRAB"),
        ("/emprego/concursos/inscricoes", citizens["concurso"], "concurso_publico", "CONC"),
        (
            "/emprego/certificacoes/profissionais",
            citizens["certificacao"],
            "certificacao_profissional",
            "CERT",
        ),
    ]
    for path, citizen_id, service_type, prefix in cases:
        response = client.post(
            path, json={"citizen_id": str(citizen_id), "metadata": {"origem": "e2e"}}
        )
        assert response.status_code == 201
        payload = response.json()
        assert payload["service_type"] == service_type
        assert payload["numero_processo"].startswith(f"{prefix}/{date.today().year}/")


@pytest.mark.integration
def test_e2e_duplicidade_workflow_ativa_retorna_400(e2e_client):
    client, citizens, _ = e2e_client
    citizen_id = citizens["oferta"]
    body = {"citizen_id": str(citizen_id), "metadata": {"canal": "portal"}}
    first = client.post("/emprego/ofertas", json=body)
    assert first.status_code == 201
    second = client.post("/emprego/ofertas", json=body)
    assert second.status_code == 400
    assert "registro ativo" in second.json()["detail"].lower()
