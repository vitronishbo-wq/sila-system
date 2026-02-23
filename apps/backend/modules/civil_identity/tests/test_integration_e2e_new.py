"""
Testes de Integração E2E para o Módulo Identidade Civil
"""

import pytest
from datetime import date
from uuid import uuid4

from app.modules.identidade_civil.domain.models.citizen import Citizen
from app.modules.identidade_civil.utils.safe import safe_get, safe_isoformat


@pytest.mark.asyncio
@pytest.mark.integration
class TestCitizenE2E:
    """Testes end-to-end para fluxo de cidadão."""
    
    async def test_citizen_entity_to_repository_flow(self, async_db_session, fuc_projection_data):
        """Testa fluxo completo: FUC Projection → Entity → Repository."""
        # 1. Criar entidade a partir da projeção FUC
        citizen = Citizen.from_fuc_projection(fuc_projection_data)
        
        assert citizen.full_name == fuc_projection_data["full_name"]
        assert citizen.is_active()
        
        # 2. Verificar dados com safe helpers
        name = safe_get(citizen, "full_name", "Unknown")
        assert name == fuc_projection_data["full_name"]
        
        # 3. Converter data com safe_isoformat
        birth_iso = safe_isoformat(citizen.birth_date)
        assert birth_iso == "2000-01-15"
    
    async def test_fuc_projection_data_transformation(self, fuc_projection_data):
        """Testa transformação de dados FUC."""
        # 1. Extrair dados com safe helpers
        name = safe_get(fuc_projection_data, "full_name", "")
        document = safe_get(fuc_projection_data, "document_number")
        birth = safe_get(fuc_projection_data, "birth_date")
        
        # 2. Criar cidadão
        citizen = Citizen(
            citizen_id=uuid4(),
            full_name=name,
            document_number=document,
            birth_date=birth,
        )
        
        # 3. Validar
        assert citizen.full_name == "João Silva"
        assert citizen.document_number == "00000000-0000-0000-0000-000000000001"
        assert citizen.birth_date == date(2000, 1, 15)
    
    async def test_multiple_citizens_workflow(self, async_db_session, fuc_projection_list):
        """Testa workflow com múltiplos cidadãos."""
        from app.modules.identidade_civil.infrastructure.repositories.citizen_repository import CitizenRepository
        
        repo = CitizenRepository(async_db_session)
        
        # 1. Criar cidadãos a partir de projeções FUC
        citizens = [
            Citizen.from_fuc_projection(fuc_data)
            for fuc_data in fuc_projection_list
        ]
        
        # 2. Verificar criação
        assert len(citizens) == len(fuc_projection_list)
        assert all(c.is_active() for c in citizens)
        
        # 3. Verificar acessibilidade com safe_get
        names = [safe_get(c, "full_name", "Unknown") for c in citizens]
        assert all(name for name in names)
        assert len(names) == 3


@pytest.mark.unit
class TestCitizenDataConsistency:
    """Testes de consistência de dados."""
    
    def test_citizen_from_fuc_preserves_all_fields(self, fuc_projection_data):
        """Testa que todos os campos são preservados."""
        citizen = Citizen.from_fuc_projection(fuc_projection_data)
        
        # Verificar cada campo
        assert str(citizen.citizen_id) == fuc_projection_data["id"]
        assert citizen.full_name == fuc_projection_data["full_name"]
        assert citizen.document_number == fuc_projection_data["document_number"]
        assert citizen.birth_date == fuc_projection_data["birth_date"]
        assert citizen.gender == fuc_projection_data["gender"]
        assert citizen.phone == fuc_projection_data["phone"]
        assert citizen.email == fuc_projection_data["email"]
        assert citizen.vital_status == fuc_projection_data["vital_status"]
    
    def test_citizen_safe_access_consistency(self, sample_citizen):
        """Testa que safe_get retorna consistentemente os dados."""
        # Acessar o mesmo campo múltiplas vezes
        result1 = safe_get(sample_citizen, "full_name")
        result2 = safe_get(sample_citizen, "full_name")
        result3 = safe_get(sample_citizen, "full_name")
        
        assert result1 == result2 == result3
        assert result1 == "João Silva"
    
    def test_citizen_missing_field_consistency(self, sample_citizen):
        """Testa que missing fields retornam consistentemente None."""
        result1 = safe_get(sample_citizen, "missing_field1")
        result2 = safe_get(sample_citizen, "missing_field2")
        
        assert result1 is None
        assert result2 is None


@pytest.mark.integration
class TestCitizenDataValidation:
    """Testes de validação de dados de cidadão."""
    
    def test_citizen_required_fields(self):
        """Testa que campos obrigatórios são validados."""
        # Tentar criar sem citizen_id deve falhar
        with pytest.raises(TypeError):
            Citizen(full_name="Test")  # type: ignore
        
        # Tentar criar sem full_name deve falhar
        with pytest.raises(TypeError):
            Citizen(citizen_id=uuid4())  # type: ignore
    
    def test_citizen_safe_instantiation_from_incomplete_fuc_data(self):
        """Testa que FUC com dados incompletos cria cidadão válido."""
        minimal_fuc = {
            "id": str(uuid4()),
            "full_name": "Minimal User"
        }
        
        citizen = Citizen.from_fuc_projection(minimal_fuc)
        
        # Deve criar com sucesso com defaults
        assert citizen.full_name == "Minimal User"
        assert citizen.vital_status == "alive"
        assert citizen.is_active()
    
    def test_citizen_active_status_validation(self):
        """Testa validação de status ativo/inativo."""
        active = Citizen(citizen_id=uuid4(), full_name="Active", vital_status="alive")
        deceased = Citizen(citizen_id=uuid4(), full_name="Deceased", vital_status="deceased")
        
        assert active.is_active() is True
        assert deceased.is_active() is False


@pytest.mark.integration
class TestCitizenServiceIntegration:
    """Testes de integração com serviços."""
    
    async def test_citizen_query_service_import(self):
        """Testa que CitizenQueryService pode ser importado."""
        from app.modules.identidade_civil.services.citizen_query_service import CitizenQueryService
        
        service = CitizenQueryService()
        assert service is not None
    
    async def test_citizen_service_import(self):
        """Testa que CitizenService pode ser importado."""
        from app.modules.identidade_civil.application.services.citizen_service import CitizenService
        
        service = CitizenService()
        assert service is not None
    
    async def test_fuc_client_import(self):
        """Testa que CitizenFUCClient pode ser importado."""
        from app.modules.identidade_civil.integrations.citizen_fuc_client import CitizenFUCClient
        
        client = CitizenFUCClient()
        assert client is not None
    
    async def test_repository_import(self):
        """Testa que CitizenRepository pode ser importado."""
        from app.modules.identidade_civil.infrastructure.repositories.citizen_repository import CitizenRepository
        
        assert CitizenRepository is not None
