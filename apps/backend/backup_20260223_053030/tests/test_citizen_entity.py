"""
Testes Unitários para Entidade Citizen
"""

import pytest
from datetime import date
from uuid import uuid4

from app.modules.identidade_civil.domain.models.citizen import Citizen
from tests.factories import CitizenFactory, InactiveCitizenFactory


class TestCitizenCreation:
    """Testes de criação da entidade Citizen"""
    
    def test_citizen_creation_with_factory(self):
        """Testa criação com factory"""
        citizen = CitizenFactory()
        
        assert citizen.citizen_id is not None
        assert citizen.full_name is not None
        assert citizen.vital_status == "alive"
    
    def test_citizen_creation_manual(self):
        """Testa criação manual"""
        citizen_id = uuid4()
        citizen = Citizen(
            citizen_id=citizen_id,
            full_name="João Silva",
            birth_date=date(2000, 1, 15),
            gender="M"
        )
        
        assert citizen.citizen_id == citizen_id
        assert citizen.full_name == "João Silva"
        assert citizen.birth_date == date(2000, 1, 15)
        assert citizen.gender == "M"
    
    def test_citizen_with_defaults(self):
        """Testa criação com valores padrão"""
        citizen = Citizen(
            citizen_id=uuid4(),
            full_name="Test"
        )
        
        assert citizen.full_name == "Test"
        assert citizen.vital_status == "alive"
        assert citizen.document_number is None
        assert citizen.birth_date is None
    
    def test_citizen_required_fields(self):
        """Testa que campos obrigatórios são validados"""
        with pytest.raises(TypeError):
            # Falta citizen_id
            Citizen(full_name="Test")  # type: ignore
        
        with pytest.raises(TypeError):
            # Falta full_name
            Citizen(citizen_id=uuid4())  # type: ignore


class TestCitizenStatus:
    """Testes para status de cidadão"""
    
    def test_citizen_is_active(self):
        """Testa cidadão ativo"""
        citizen = CitizenFactory(vital_status="alive")
        assert citizen.is_active() is True
    
    def test_citizen_is_inactive(self):
        """Testa cidadão inativo"""
        citizen = InactiveCitizenFactory()
        assert citizen.is_active() is False
    
    def test_different_vital_statuses(self):
        """Testa diferentes status vitais"""
        statuses = ["alive", "deceased", "missing"]
        
        for status in statuses:
            citizen = CitizenFactory(vital_status=status)
            assert citizen.vital_status == status
            assert citizen.is_active() == (status == "alive")


class TestCitizenFromFUC:
    """Testes para factory method from_fuc_projection"""
    
    def test_from_fuc_projection_complete(self):
        """Testa com dados FUC completos"""
        fuc_data = {
            "id": str(uuid4()),
            "full_name": "Maria Santos",
            "document_number": "12345678",
            "birth_date": date(1995, 5, 20),
            "gender": "F",
            "phone": "+244912345678",
            "email": "maria@example.com",
            "vital_status": "alive",
        }
        
        citizen = Citizen.from_fuc_projection(fuc_data)
        
        assert str(citizen.citizen_id) == fuc_data["id"]
        assert citizen.full_name == fuc_data["full_name"]
        assert citizen.document_number == fuc_data["document_number"]
        assert citizen.birth_date == fuc_data["birth_date"]
        assert citizen.gender == fuc_data["gender"]
        assert citizen.phone == fuc_data["phone"]
        assert citizen.email == fuc_data["email"]
        assert citizen.vital_status == fuc_data["vital_status"]
    
    def test_from_fuc_projection_minimal(self):
        """Testa com dados FUC mínimos"""
        fuc_data = {
            "id": str(uuid4()),
            "full_name": "Minimal User"
        }
        
        citizen = Citizen.from_fuc_projection(fuc_data)
        
        assert citizen.full_name == "Minimal User"
        assert citizen.vital_status == "alive"
        assert citizen.document_number is None
    
    def test_from_fuc_projection_with_missing_fields(self):
        """Testa com campos faltando"""
        fuc_data = {
            "id": str(uuid4()),
            "full_name": "Test",
            "gender": "M",
            # Faltam outros campos
        }
        
        citizen = Citizen.from_fuc_projection(fuc_data)
        
        assert citizen.full_name == "Test"
        assert citizen.gender == "M"
        assert citizen.birth_date is None
        assert citizen.email is None


class TestCitizenRepresentation:
    """Testes para representações da entidade"""
    
    def test_citizen_str(self):
        """Testa __str__"""
        citizen = CitizenFactory(full_name="João Silva")
        str_repr = str(citizen)
        
        assert "Citizen" in str_repr
        assert "João Silva" in str_repr
    
    def test_citizen_repr(self):
        """Testa __repr__"""
        citizen = CitizenFactory(full_name="João Silva")
        repr_str = repr(citizen)
        
        assert "Citizen" in repr_str
        assert "João Silva" in repr_str


class TestCitizenEquality:
    """Testes para igualdade entre Citizens"""
    
    def test_citizen_equality(self):
        """Testa igualdade com mesmo ID"""
        citizen_id = uuid4()
        
        citizen1 = Citizen(citizen_id=citizen_id, full_name="Name")
        citizen2 = Citizen(citizen_id=citizen_id, full_name="Name")
        
        assert citizen1 == citizen2
    
    def test_citizen_inequality(self):
        """Testa desigualdade com IDs diferentes"""
        citizen1 = CitizenFactory()
        citizen2 = CitizenFactory()
        
        assert citizen1 != citizen2
