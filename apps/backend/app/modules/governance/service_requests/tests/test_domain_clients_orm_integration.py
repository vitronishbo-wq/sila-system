from __future__ import annotations

from datetime import date
from uuid import uuid4

import pytest

from apps.backend.app.core.bridges import CitizenRepository
from apps.backend.app.core.bridges.identity_bridge import CitizenFUC
from apps.backend.app.core.bridges.society_domain_enums_bridge import (
    EscolaridadeEmprego,
    EscolaridadeJuventude,
    FaixaEtaria,
    FaixaVulnerabilidade,
    HealthUnitType,
    SituacaoBeneficiario,
    SituacaoOcupacional,
    SituacaoProfissional,
    StatusCandidato,
    StatusMatricula,
    StatusPrograma,
    TipoPrograma,
    Turno,
)
from apps.backend.app.core.bridges.society_repository_bridges import (
    make_assistencia_beneficiario_repository,
    make_educacao_turma_repository,
    make_emprego_candidato_repository,
    make_juventude_jovem_repository,
    make_juventude_programa_repository,
    make_saude_health_unit_repository,
)
from apps.backend.app.core.bridges.society_statistics_models_bridge import (
    BeneficiarioModel,
    CandidatoModel,
    HealthUnitModel,
    JovemModel,
    MatriculaModel,
    ProgramaJuvenilModel,
    TurmaModel,
)
from apps.backend.app.modules.governance.service_requests.domain.enums import ServiceType
from apps.backend.app.modules.governance.service_requests.infrastructure.clients.assistencia_client import (
    AssistenciaClient,
)
from apps.backend.app.modules.governance.service_requests.infrastructure.clients.educacao_client import (
    EducacaoClient,
)
from apps.backend.app.modules.governance.service_requests.infrastructure.clients.emprego_client import (
    EmpregoClient,
)
from apps.backend.app.modules.governance.service_requests.infrastructure.clients.identidade_client import (
    IdentidadeClient,
)
from apps.backend.app.modules.governance.service_requests.infrastructure.clients.juventude_client import (
    JuventudeClient,
)
from apps.backend.app.modules.governance.service_requests.infrastructure.clients.saude_client import (
    SaudeClient,
)


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.db
async def test_identidade_client_validate_payload_with_real_repository(db_session) -> None:
    citizen_id = uuid4()
    db_session.add(
        CitizenFUC(
            citizen_id=citizen_id,
            full_name="Cidadao Integracao Identidade",
            is_active=True,
            vital_status="alive",
            document_number=f"BI-{citizen_id.hex[:8]}",
        )
    )
    await db_session.flush()
    client = IdentidadeClient(citizen_repo=CitizenRepository(db_session))
    ok, reason = await client.validate_payload(
        service_type=ServiceType.GENERAL_SUPPORT.value, citizen_id=citizen_id, payload={}
    )
    submitted = await client.submit(
        service_type=ServiceType.GENERAL_SUPPORT.value,
        request_id=uuid4(),
        citizen_id=citizen_id,
        payload={},
    )
    assert ok is True
    assert reason is None
    assert submitted["module"] == "identidade_civil"
    assert submitted["accepted"] is True


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.db
async def test_educacao_client_validate_and_submit_with_real_repositories(db_session) -> None:
    citizen_id = uuid4()
    turma_id = uuid4()
    ano_letivo_id = uuid4()
    escola_id = uuid4()
    db_session.add(
        TurmaModel(
            id=turma_id,
            escola_id=escola_id,
            ano_letivo_id=ano_letivo_id,
            codigo=f"TURMA-{turma_id.hex[:6]}",
            classe="1A",
            turno=Turno.MANHA.value,
            capacidade=2,
            ativa=True,
        )
    )
    db_session.add(
        MatriculaModel(
            id=uuid4(),
            numero_processo=f"MAT-{uuid4().hex[:10]}",
            citizen_id=uuid4(),
            escola_id=escola_id,
            turma_id=turma_id,
            ano_letivo_id=ano_letivo_id,
            data_matricula=date.today(),
            status=StatusMatricula.ATIVA.value,
            observacoes=None,
        )
    )
    await db_session.flush()
    client = EducacaoClient(turma_repo=make_educacao_turma_repository(db_session))
    payload = {"turma_id": str(turma_id), "ano_letivo_id": str(ano_letivo_id)}
    ok, reason = await client.validate_payload(
        service_type=ServiceType.EDUCATION_ENROLLMENT.value, citizen_id=citizen_id, payload=payload
    )
    submitted = await client.submit(
        service_type=ServiceType.EDUCATION_ENROLLMENT.value,
        request_id=uuid4(),
        citizen_id=citizen_id,
        payload=payload,
    )
    assert ok is True
    assert reason is None
    assert submitted["module"] == "educacao"
    assert submitted["vaga_disponivel"] is True
    assert submitted["vagas_restantes"] == 1


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.db
async def test_juventude_client_validate_and_submit_with_real_repositories(db_session) -> None:
    citizen_id = uuid4()
    programa_id = uuid4()
    db_session.add(
        JovemModel(
            id=uuid4(),
            numero_registro=f"JOV-{uuid4().hex[:8]}",
            nome="Jovem Integracao",
            data_nascimento=date(2004, 1, 1),
            faixa_etaria=FaixaEtaria.JOVEM_18_24.value,
            genero="M",
            naturalidade="Huambo",
            nacionalidade="Angolana",
            escolaridade=EscolaridadeJuventude.MEDIO_COMPLETO.value,
            situacao_ocupacional=SituacaoOcupacional.PROCURA_EMPREGO.value,
            endereco="Rua A",
            municipio="Huambo",
            provincia="Huambo",
            citizen_id=citizen_id,
            data_cadastro=date.today(),
            ativo=True,
        )
    )
    db_session.add(
        ProgramaJuvenilModel(
            id=programa_id,
            codigo_programa=f"PRG-{uuid4().hex[:8]}",
            nome="Programa Integracao",
            tipo=TipoPrograma.CAPACITACAO.value,
            data_inicio=date.today(),
            data_fim=None,
            vagas=50,
            municipio="Huambo",
            provincia="Huambo",
            status=StatusPrograma.INSCRICOES_ABERTAS.value,
            data_cadastro=date.today(),
            observacoes=None,
            ativo=True,
        )
    )
    await db_session.flush()
    client = JuventudeClient(
        jovem_repo=make_juventude_jovem_repository(db_session),
        programa_repo=make_juventude_programa_repository(db_session),
    )
    payload = {"programa_id": str(programa_id)}
    ok, reason = await client.validate_payload(
        service_type=ServiceType.YOUTH_PROGRAM.value, citizen_id=citizen_id, payload=payload
    )
    submitted = await client.submit(
        service_type=ServiceType.YOUTH_PROGRAM.value,
        request_id=uuid4(),
        citizen_id=citizen_id,
        payload=payload,
    )
    assert ok is True
    assert reason is None
    assert submitted["module"] == "juventude"
    assert submitted["programa_id"] == str(programa_id)


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.db
async def test_emprego_client_validate_and_submit_with_real_repositories(db_session) -> None:
    citizen_id = uuid4()
    candidato_id = uuid4()
    db_session.add(
        CandidatoModel(
            id=candidato_id,
            numero_processo=f"CAND-{uuid4().hex[:8]}",
            citizen_id=citizen_id,
            data_registro=date.today(),
            escolaridade=EscolaridadeEmprego.SECUNDARIA.value,
            situacao=SituacaoProfissional.DESEMPREGADO.value,
            areas_interesse=["tecnologia"],
            experiencias=[],
            habilidades=["python"],
            status=StatusCandidato.ATIVO.value,
            observacoes=None,
        )
    )
    await db_session.flush()
    client = EmpregoClient(candidato_repo=make_emprego_candidato_repository(db_session))
    payload = {"vaga_id": str(uuid4())}
    ok, reason = await client.validate_payload(
        service_type=ServiceType.EMPLOYMENT_APPLICATION.value,
        citizen_id=citizen_id,
        payload=payload,
    )
    submitted = await client.submit(
        service_type=ServiceType.EMPLOYMENT_APPLICATION.value,
        request_id=uuid4(),
        citizen_id=citizen_id,
        payload=payload,
    )
    assert ok is True
    assert reason is None
    assert submitted["module"] == "emprego"
    assert submitted["candidato_id"] == str(candidato_id)


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.db
async def test_saude_client_validate_and_submit_with_real_repositories(db_session) -> None:
    citizen_id = uuid4()
    health_unit_id = uuid4()
    db_session.add(
        HealthUnitModel(
            id=health_unit_id,
            code=f"HU-{uuid4().hex[:6]}",
            name="Unidade Integracao",
            unit_type=HealthUnitType.HEALTH_CENTER.value,
            province="Huambo",
            municipality="Huambo",
            commune="Huambo",
            address="Rua da Unidade",
            phone=None,
            email=None,
            beds=10,
            has_emergency=True,
            has_laboratory=True,
            has_pharmacy=True,
            specialties=["clinica_geral"],
            opening_hours={"seg-sex": "08:00-17:00"},
            metadata_={},
            is_active=True,
        )
    )
    await db_session.flush()
    client = SaudeClient(health_unit_repo=make_saude_health_unit_repository(db_session))
    payload = {"health_unit_id": str(health_unit_id)}
    ok, reason = await client.validate_payload(
        service_type=ServiceType.HEALTH_APPOINTMENT.value, citizen_id=citizen_id, payload=payload
    )
    submitted = await client.submit(
        service_type=ServiceType.HEALTH_APPOINTMENT.value,
        request_id=uuid4(),
        citizen_id=citizen_id,
        payload=payload,
    )
    assert ok is True
    assert reason is None
    assert submitted["module"] == "saude"
    assert submitted["health_unit_id"] == str(health_unit_id)


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.db
async def test_assistencia_client_validate_and_submit_with_real_repositories(db_session) -> None:
    citizen_id = uuid4()
    beneficiario_id = uuid4()
    db_session.add(
        BeneficiarioModel(
            id=beneficiario_id,
            numero_registro=f"BEN-{uuid4().hex[:8]}",
            citizen_id=citizen_id,
            cadastro_unico_id=None,
            faixa_vulnerabilidade=FaixaVulnerabilidade.ALTA.value,
            situacao=SituacaoBeneficiario.ATIVO.value,
            data_cadastro=date.today(),
            observacoes=None,
            ativo=True,
        )
    )
    await db_session.flush()
    client = AssistenciaClient(
        beneficiario_repo=make_assistencia_beneficiario_repository(db_session)
    )
    ok, reason = await client.validate_payload(
        service_type=ServiceType.SOCIAL_BENEFIT.value, citizen_id=citizen_id, payload={}
    )
    submitted = await client.submit(
        service_type=ServiceType.SOCIAL_BENEFIT.value,
        request_id=uuid4(),
        citizen_id=citizen_id,
        payload={},
    )
    assert ok is True
    assert reason is None
    assert submitted["module"] == "assistencia_social"
    assert submitted["beneficiario_id"] == str(beneficiario_id)
