"""
Testes Unitários para a Entidade de Domínio Citizen
"""

import pytest
from datetime import date, datetime
from uuid import uuid4

from app.modules.identidade_civil.domain.models.citizen import Citizen


@pytest.mark.unit
class TestCitizenEntity:
    """Testes para a entidade Citizen."""
    
    def test_citizen_creation(self, sample_citizen):
        """Testa criação básica de um Citizen."""
        assert sample_citizen.citizen_id is not None
        assert sample_citizen.full_name == "João Silva"
        assert sample_citizen.document_number == "00000000-0000-0000-0000-000000000001"
        assert sample_citizen.birth_date == date(2000, 1, 15)
        assert sample_citizen.gender == "M"
        assert sample_citizen.phone == "+244912345678"
        assert sample_citizen.email == "joao.silva@example.com"
        assert sample_citizen.vital_status == "alive"
    
    def test_citizen_creation_with_defaults(self):
        """Testa criação de Citizen com valores padrão."""
        citizen = Citizen(
            citizen_id=uuid4(),
            full_name="Test User"
        )
        
        assert citizen.document_number is None
        assert citizen.birth_date is None
        assert citizen.gender is None
        assert citizen.phone is None
        assert citizen.email is None
        assert citizen.vital_status == "alive"
        assert citizen.fuc_sync_timestamp is None
        assert citizen.created_at is not None
    
    def test_citizen_str_representation(self, sample_citizen):
        """Testa representação em string."""
        citizen_str = str(sample_citizen)
        assert "Citizen" in citizen_str
        assert sample_citizen.citizen_id in citizen_str or str(sample_citizen.citizen_id) in citizen_str
        assert "João Silva" in citizen_str
    
    def test_citizen_repr(self, sample_citizen):
        """Testa representação para debugging."""
        citizen_repr = repr(sample_citizen)
        assert "Citizen" in citizen_repr
        assert "João Silva" in citizen_repr
    
    def test_citizen_is_active(self, sample_citizen, sample_inactive_citizen):
        """Testa método is_active()."""
        assert sample_citizen.is_active() is True
        assert sample_inactive_citizen.is_active() is False
    
    def test_citizen_from_fuc_projection(self, fuc_projection_data):
        """Testa factory method from_fuc_projection."""
        citizen = Citizen.from_fuc_projection(fuc_projection_data)
        
        assert str(citizen.citizen_id) == fuc_projection_data["id"]
        assert citizen.full_name == fuc_projection_data["full_name"]
        assert citizen.document_number == fuc_projection_data["document_number"]
        assert citizen.birth_date == fuc_projection_data["birth_date"]
        assert citizen.gender == fuc_projection_data["gender"]
        assert citizen.phone == fuc_projection_data["phone"]
        assert citizen.email == fuc_projection_data["email"]
        assert citizen.vital_status == fuc_projection_data["vital_status"]
        assert citizen.fuc_sync_timestamp is not None
    
    def test_citizen_from_fuc_projection_with_missing_fields(self):
        """Testa factory method com campos faltando."""
        fuc_data = {
            "id": str(uuid4()),
            "full_name": "Incomplete User"
        }
        
        citizen = Citizen.from_fuc_projection(fuc_data)
        
        assert citizen.full_name == "Incomplete User"
        assert citizen.document_number is None
        assert citizen.birth_date is None
        assert citizen.gender is None
        assert citizen.phone is None
        assert citizen.email is None
        assert citizen.vital_status == "alive"
    
    def test_citizen_equality(self):
        """Testa igualdade entre Citizen instances."""
        citizen_id = uuid4()
        
        citizen1 = Citizen(
            citizen_id=citizen_id,
            full_name="Same User"
        )
        
        citizen2 = Citizen(
            citizen_id=citizen_id,
            full_name="Same User"
        )
        
        # Dataclasses com mesmo ID e nome devem ser iguais
        assert citizen1 == citizen2
    
    def test_citizen_with_incomplete_data(self):
        """Testa criação com dados incompletos."""
        citizen = Citizen(
            citizen_id=uuid4(),
            full_name="Only Name"
        )
        
        assert citizen.full_name == "Only Name"
        assert citizen.document_number is None
        assert citizen.gender is None
        assert citizen.vital_status == "alive"
        assert citizen.is_active()
    
    def test_citizen_timestamps(self, sample_citizen):
        """Testa que timestamps são gerados."""
        assert isinstance(sample_citizen.created_at, datetime)
        assert isinstance(sample_citizen.updated_at, datetime)
        assert sample_citizen.created_at <= sample_citizen.updated_at


@pytest.mark.unit
class TestCitizenValidation:
    """Testes para validação de dados do Citizen."""
    
    def test_citizen_full_name_required(self):
        """Testa que full_name é obrigatório."""
        with pytest.raises(TypeError):
            # Dataclass vai lançar TypeError se field obrigatório faltar
            Citizen(citizen_id=uuid4())  # type: ignore
    
    def test_citizen_citizen_id_required(self):
        """Testa que citizen_id é obrigatório."""
        with pytest.raises(TypeError):
            Citizen(full_name="Test")  # type: ignore
    
    def test_citizen_gender_values(self):
        """Testa que gender pode ter diferentes valores."""
        genders = ["M", "F", "O", "X", None]
        
        for gender in genders:
            citizen = Citizen(
                citizen_id=uuid4(),
                full_name="Test",
                gender=gender
            )
            assert citizen.gender == gender
    
    def test_citizen_vital_status_values(self):
        """Testa diferentes valores de vital_status."""
        statuses = ["alive", "deceased", "missing", "unknown"]
        
        for status in statuses:
            citizen = Citizen(
                citizen_id=uuid4(),
                full_name="Test",
                vital_status=status
            )
            assert citizen.vital_status == status


@pytest.mark.unit
class TestCitizenDataTransformation:
    """Testes para transformação de dados do Citizen."""
    
    def test_citizen_to_dict(self, sample_citizen_list):
        """Testa transformação de Citizen para dicionário (se implementado)."""
        # Este teste é preparado para para quando to_dict for adicionado
        citizen = sample_citizen_list[0]
        
        # Verificar que os atributos principais estão acessíveis
        assert hasattr(citizen, "citizen_id")
        assert hasattr(citizen, "full_name")
        assert hasattr(citizen, "document_number")
    
    def test_citizen_immutability_options(self):
        """Testa comportamento de mutabilidade do dataclass."""
        citizen = Citizen(
            citizen_id=uuid4(),
            full_name="Immutable Test"
        )
        
        # Dataclasses padrão são mutáveis
        original_name = citizen.full_name
        citizen.full_name = "Modified"
        
        assert citizen.full_name == "Modified"
        assert citizen.full_name != original_name
