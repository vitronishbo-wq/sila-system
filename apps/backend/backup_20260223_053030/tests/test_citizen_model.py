"""
Testes para Modelo SQLAlchemy CitizenModel
"""

import pytest
from datetime import date, datetime
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.modules.identidade_civil.infrastructure.models.citizen_model import CitizenModel
from tests.factories import CitizenModelFactory


@pytest.fixture(scope="module")
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    CitizenModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


class TestCitizenModelBasic:
    """Testes básicos do modelo"""
    
    def test_citizen_model_creation(self, db):
        """Testa criação do modelo usando factory"""
        citizen = CitizenModelFactory(
            sqlalchemy_session=db,
            full_name="Test User"
        )
        
        assert citizen.citizen_id is not None
        assert citizen.full_name == "Test User"
        assert citizen.vital_status == "alive"
    
    def test_citizen_model_manual_creation(self, db):
        """Testa criação manual"""
        from uuid import uuid4
        
        citizen = CitizenModel(
            citizen_id=uuid4(),
            full_name="Manual User",
            birth_date=date(2000, 1, 1),
            gender="M"
        )
        
        db.add(citizen)
        db.commit()
        
        assert citizen.full_name == "Manual User"
        assert citizen.gender == "M"
    
    def test_citizen_model_with_all_fields(self, db):
        """Testa modelo com todos os campos"""
        from uuid import uuid4
        
        citizen = CitizenModel(
            citizen_id=uuid4(),
            full_name="Full User",
            document_number="12345678",
            birth_date=date(1990, 5, 15),
            gender="F",
            phone="+244912345678",
            email="user@example.com",
            vital_status="alive"
        )
        
        db.add(citizen)
        db.commit()
        
        assert citizen.full_name == "Full User"
        assert citizen.document_number == "12345678"
        assert citizen.gender == "F"
        assert citizen.email == "user@example.com"


class TestCitizenModelConversion:
    """Testes de conversão do modelo"""
    
    def test_citizen_model_to_dict(self, db):
        """Testa conversão para dicionário"""
        citizen = CitizenModelFactory(
            sqlalchemy_session=db,
            full_name="Dict Test"
        )
        
        db.commit()
        
        dict_repr = citizen.to_dict()
        
        assert isinstance(dict_repr, dict)
        assert dict_repr["full_name"] == "Dict Test"
        assert dict_repr["citizen_id"] == str(citizen.citizen_id)
        assert dict_repr["vital_status"] == "alive"
    
    def test_citizen_model_to_dict_with_dates(self, db):
        """Testa conversão com datas"""
        from uuid import uuid4
        
        birth_date = date(1995, 3, 20)
        citizen = CitizenModel(
            citizen_id=uuid4(),
            full_name="Date Test",
            birth_date=birth_date
        )
        
        db.add(citizen)
        db.commit()
        
        dict_repr = citizen.to_dict()
        
        # Datas devem ser convertidas para ISO string
        assert dict_repr["birth_date"] == "1995-03-20"


class TestCitizenModelStringRep:
    """Testes para representações em string"""
    
    def test_citizen_model_str(self, db):
        """Testa __str__"""
        citizen = CitizenModelFactory(
            sqlalchemy_session=db,
            full_name="String Test"
        )
        
        str_repr = str(citizen)
        
        assert "Citizen" in str_repr
        assert "String Test" in str_repr
    
    def test_citizen_model_repr(self, db):
        """Testa __repr__"""
        citizen = CitizenModelFactory(
            sqlalchemy_session=db,
            full_name="Repr Test"
        )
        
        repr_str = repr(citizen)
        
        assert "CitizenModel" in repr_str
        assert "Repr Test" in repr_str


class TestCitizenModelAttributes:
    """Testes para atributos específicos"""
    
    def test_vital_status_default(self, db):
        """Testa default de vital_status"""
        from uuid import uuid4
        
        citizen = CitizenModel(
            citizen_id=uuid4(),
            full_name="Default Test"
        )
        
        assert citizen.vital_status == "alive"
    
    def test_vital_status_custom(self, db):
        """Testa vital_status customizado"""
        from uuid import uuid4
        
        citizen = CitizenModel(
            citizen_id=uuid4(),
            full_name="Custom Test",
            vital_status="deceased"
        )
        
        assert citizen.vital_status == "deceased"
    
    def test_timestamps_present(self, db):
        """Testa que timestamps estão presentes"""
        citizen = CitizenModelFactory(sqlalchemy_session=db)
        
        db.commit()
        
        assert isinstance(citizen.created_at, datetime)
        assert isinstance(citizen.updated_at, datetime)
    
    def test_optional_fields_nullable(self, db):
        """Testa que campos opcionais podem ser None"""
        from uuid import uuid4
        
        citizen = CitizenModel(
            citizen_id=uuid4(),
            full_name="Nullable Test"
        )
        
        db.add(citizen)
        db.commit()
        
        assert citizen.document_number is None
        assert citizen.birth_date is None
        assert citizen.gender is None
        assert citizen.phone is None
        assert citizen.email is None


class TestCitizenModelMutability:
    """Testes para mutabilidade do modelo"""
    
    def test_citizen_model_modification(self, db):
        """Testa modificação de modelo"""
        citizen = CitizenModelFactory(
            sqlalchemy_session=db,
            full_name="Original"
        )
        
        citizen.full_name = "Modified"
        db.commit()
        
        assert citizen.full_name == "Modified"
    
    def test_citizen_model_persist_modification(self, db):
        """Testa que modificações são persistidas"""
        from uuid import uuid4
        
        citizen = CitizenModel(
            citizen_id=uuid4(),
            full_name="Persist Test",
            phone="+244912345678"
        )
        
        db.add(citizen)
        db.commit()
        
        # Modificar
        original_id = citizen.citizen_id
        citizen.phone = "+244987654321"
        db.commit()
        
        # Recuperar do banco
        retrieved = db.query(CitizenModel).filter_by(citizen_id=original_id).first()
        
        assert retrieved.phone == "+244987654321"


class TestCitizenModelAdvanced:
    """Testes avançados para o modelo"""
    
    def test_create_citizen_minimal(self, in_memory_db):
        citizen = CitizenModel(
            citizen_id=uuid4(),
            national_id_number="123456789",
            nif="987654321",
            first_name="João",
            last_name="Silva",
            full_name="João Silva",
            gender="M",
            birth_date=date(1990, 1, 1),
            marital_status="SINGLE",
            nationality="Angolana",
            place_of_birth="Luanda",
            father_name="Carlos Silva",
            mother_name="Maria Silva",
            phone="999999999",
            email="joao@email.com",
            province="Luanda",
            municipality="Luanda",
            commune="Maianga",
            neighborhood="Bairro Azul",
            street="Rua Principal",
            house_number="123",
            status="ACTIVE",
            is_verified=False,
            verification_level="BASIC",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by="admin",
            updated_by="admin"
        )
        in_memory_db.add(citizen)
        in_memory_db.commit()
        assert citizen.citizen_id is not None
        assert citizen.full_name == "João Silva"
    
    def test_unique_constraints(self, in_memory_db):
        citizen1 = CitizenModel(
            citizen_id=uuid4(),
            national_id_number="111",
            nif="222",
            first_name="A",
            last_name="B",
            full_name="A B",
            gender="F",
            birth_date=date(1991, 2, 2),
            marital_status="SINGLE",
            nationality="Angolana",
            place_of_birth="Benguela",
            father_name="F1",
            mother_name="M1",
            phone="888888888",
            email="a@email.com",
            province="Benguela",
            municipality="Benguela",
            commune="Centro",
            neighborhood="Centro",
            street="Rua 1",
            house_number="1",
            status="ACTIVE",
            is_verified=True,
            verification_level="BASIC",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by="admin",
            updated_by="admin"
        )
        in_memory_db.add(citizen1)
        in_memory_db.commit()
        citizen2 = CitizenModel(
            citizen_id=uuid4(),
            national_id_number="111",  # Duplicate
            nif="333",
            first_name="C",
            last_name="D",
            full_name="C D",
            gender="O",
            birth_date=date(1992, 3, 3),
            marital_status="MARRIED",
            nationality="Angolana",
            place_of_birth="Huambo",
            father_name="F2",
            mother_name="M2",
            phone="777777777",
            email="c@email.com",
            province="Huambo",
            municipality="Huambo",
            commune="Centro",
            neighborhood="Centro",
            street="Rua 2",
            house_number="2",
            status="INACTIVE",
            is_verified=False,
            verification_level="BASIC",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by="admin",
            updated_by="admin"
        )
        in_memory_db.add(citizen2)
        with pytest.raises(IntegrityError):
            in_memory_db.commit()
            in_memory_db.rollback()
