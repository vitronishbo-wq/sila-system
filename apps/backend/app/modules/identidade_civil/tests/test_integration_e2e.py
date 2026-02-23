"""
Testes de Integração E2E - Módulo Identidade Civil

Testes end-to-end com setup de banco de dados, fixtures reais
e fluxos completos de negócio.
"""
import pytest
import uuid
from datetime import date, datetime


from app.modules.identidade_civil.domain.models.bi_record import BIRecord
from app.modules.identidade_civil.domain.models.identity_request import IdentityRequest
from app.modules.identidade_civil.infrastructure.repositories.bi_repository import BIRepository
from app.modules.identidade_civil.infrastructure.repositories.identity_request_repository import IdentityRequestRepository
from app.modules.identidade_civil.services.bi_emission_service import BIEmissionService
from app.modules.identidade_civil.integrations.citizen_fuc_client import CitizenFUCClient
from app.modules.identidade_civil.exceptions import BusinessRuleException, SovereigntyValidationException


# Esta bateria de testes reusa a fixture `db_session` definida em
# `tests/conftest.py`, que cria uma sessão assíncrona apontando para o
# Postgres de teste e garante rollback após cada caso de teste.


@pytest.fixture
async def bi_repository(db_session: AsyncSession):
    """Cria repositório de BI."""
    return BIRepository(db_session)


@pytest.fixture
async def ir_repository(db_session: AsyncSession):
    """Cria repositório de IdentityRequest."""
    return IdentityRequestRepository(db_session)


@pytest.fixture
async def mock_fuc_client():
    """Mock do cliente FUC."""
    class MockFUCClient(CitizenFUCClient):
        async def get_citizen_by_id(self, citizen_fuc_id: str):
            if citizen_fuc_id == "INVALID-ID":
                return None
            
            class MockProjection:
                full_name = "João da Silva"
                birth_date = date(1980, 1, 1)
                vital_status = "alive"
                sync_timestamp = datetime.utcnow()
            
            return MockProjection()
        
        async def validate_eligibility(self, citizen_fuc_id: str, service_code: str):
            return citizen_fuc_id != "INELIGIBLE-ID"
        
        async def get_sovereignty_projection(self, citizen_fuc_id: str):
            if citizen_fuc_id == "INVALID-ID":
                return None
            
            class MockProjection:
                full_name = "Maria da Silva"
                birth_date = date(1975, 5, 15)
                vital_status = "alive"
                sync_timestamp = datetime.utcnow()
            
            return MockProjection()
    
    return MockFUCClient()


@pytest.fixture
async def bi_emission_service(db_session: AsyncSession, mock_fuc_client):
    """Cria serviço de emissão de BI."""
    return BIEmissionService(db_session, mock_fuc_client)


# Testes de Integração E2E


@pytest.mark.asyncio
class TestBIEmissionServiceE2E:
    """Testes end-to-end do serviço de emissão de BI."""

    async def test_successful_emission_flow(
        self,
        bi_emission_service: BIEmissionService,
        ir_repository: IdentityRequestRepository,
    ):
        """Teste completo de emissão de BI com sucesso."""
        citizen_fuc_id = "CITIZEN-123456"
        operator_id = "OP-001"
        
        # Executar emissão
        result = await bi_emission_service.execute_emission(
            citizen_fuc_id=citizen_fuc_id,
            operator_id=operator_id,
            notes="Teste de emissão E2E"
        )
        
        # Validar resultado
        assert result["success"] is True
        assert result["status"] == "approved"
        assert "request_id" in result
        assert "citizen_name" in result
        
        # Validar persistência
        request_id = uuid.UUID(result["request_id"])
        request = await ir_repository.get_by_id(request_id)
        
        assert request is not None
        assert request.citizen_fuc_id == citizen_fuc_id
        assert request.service_code == "001"
        assert request.status == "approved"
        assert len(request.notes) >= 2

    async def test_emission_with_sovereign_not_found(
        self,
        bi_emission_service: BIEmissionService,
    ):
        """Teste de emissão com cidadão não localizado.no FUC."""
        citizen_fuc_id = "INVALID-ID"
        operator_id = "OP-001"
        
        # Deve falhar
        with pytest.raises(SovereigntyValidationException):
            await bi_emission_service.execute_emission(
                citizen_fuc_id=citizen_fuc_id,
                operator_id=operator_id,
            )

    async def test_emission_with_ineligible_citizen(
        self,
        bi_emission_service: BIEmissionService,
    ):
        """Teste de emissão com cidadão não elegível."""
        citizen_fuc_id = "INELIGIBLE-ID"
        operator_id = "OP-001"
        
        # Deve falhar
        with pytest.raises(BusinessRuleException):
            await bi_emission_service.execute_emission(
                citizen_fuc_id=citizen_fuc_id,
                operator_id=operator_id,
            )

    async def test_emission_with_existing_active_bi(
        self,
        bi_emission_service: BIEmissionService,
        bi_repository: BIRepository,
        db_session: AsyncSession,
    ):
        """Teste de emissão quando já existe BI ativo."""
        citizen_fuc_id = "CITIZEN-WITH-ACTIVE-BI"
        operator_id = "OP-001"
        
        # Criar BI ativo existente
        existing_bi = BIRecord(
            id=uuid.uuid4(),
            citizen_fuc_id=citizen_fuc_id,
            bi_number="123456789AB001",
            issue_date=date.today(),
            status="active"
        )
        await bi_repository.save(existing_bi)
        
        # Tentar emitir novamente deve falhar
        with pytest.raises(BusinessRuleException) as exc_info:
            await bi_emission_service.execute_emission(
                citizen_fuc_id=citizen_fuc_id,
                operator_id=operator_id,
            )
        
        assert "BI ativo" in str(exc_info.value.detail)


@pytest.mark.asyncio
class TestBIRepository:
    """Testes do repositório de BI."""

    async def test_save_and_retrieve_bi(
        self,
        bi_repository: BIRepository,
    ):
        """Teste de salvar e recuperar BI."""
        bi_id = uuid.uuid4()
        bi = BIRecord(
            id=bi_id,
            citizen_fuc_id="CITIZEN-001",
            bi_number="123456789AB001",
            issue_date=date.today(),
            status="active"
        )
        
        # Salvar
        saved_bi = await bi_repository.save(bi)
        assert saved_bi.id == bi_id
        assert saved_bi.version == 1
        
        # Recuperar por ID
        retrieved = await bi_repository.get_by_id(bi_id)
        assert retrieved is not None
        assert retrieved.bi_number == "123456789AB001"

    async def test_get_by_citizen(
        self,
        bi_repository: BIRepository,
    ):
        """Teste de listar BIs por cidadão."""
        citizen_fuc_id = "CITIZEN-002"
        
        # Criar múltiplos BIs
        for i in range(3):
            bi = BIRecord(
                id=uuid.uuid4(),
                citizen_fuc_id=citizen_fuc_id,
                bi_number=f"123456789AB{i:03d}",
                issue_date=date.today(),
                status="active"
            )
            await bi_repository.save(bi)
        
        # Listar
        bis = await bi_repository.get_by_citizen(citizen_fuc_id)
        assert len(bis) == 3

    async def test_update_status(
        self,
        bi_repository: BIRepository,
    ):
        """Teste de atualização de status."""
        bi = BIRecord(
            id=uuid.uuid4(),
            citizen_fuc_id="CITIZEN-003",
            bi_number="123456789AB999",
            issue_date=date.today(),
            status="active"
        )
        
        saved_bi = await bi_repository.save(bi)
        
        # Atualizar status
        updated = await bi_repository.update_status(
            saved_bi.id,
            "suspended",
            reason="Teste de suspensão"
        )
        
        assert updated.status == "suspended"
        assert updated.reason_for_status == "Teste de suspensão"
        assert updated.version == 2


@pytest.mark.asyncio
class TestIdentityRequestRepository:
    """Testes do repositório de IdentityRequest."""

    async def test_save_and_retrieve_request(
        self,
        ir_repository: IdentityRequestRepository,
    ):
        """Teste de salvar e recuperar requisição."""
        request_id = uuid.uuid4()
        request = IdentityRequest(
            id=request_id,
            citizen_fuc_id="CITIZEN-004",
            service_code="001",
            status="pending",
            notes=["Teste inicial"]
        )
        
        saved = await ir_repository.save(request)
        assert saved.id == request_id
        
        retrieved = await ir_repository.get_by_id(request_id)
        assert retrieved is not None
        assert retrieved.service_code == "001"

    async def test_get_pending_requests(
        self,
        ir_repository: IdentityRequestRepository,
    ):
        """Teste de listar requisições pendentes."""
        # Criar requisições
        for status in ["pending", "approved", "pending_fuc_validation"]:
            request = IdentityRequest(
                id=uuid.uuid4(),
                citizen_fuc_id="CITIZEN-005",
                service_code="001",
                status=status,
            )
            await ir_repository.save(request)
        
        # Listar pendentes
        pending = await ir_repository.get_pending()
        assert len(pending) == 2  # pending + pending_fuc_validation
