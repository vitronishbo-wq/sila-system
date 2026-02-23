"""
Testes para CitizenRepository
"""

import pytest
from uuid import uuid4

from app.modules.identidade_civil.infrastructure.repositories.citizen_repository import CitizenRepository
from app.citizen.core.models import CitizenFUC
from tests.factories import CitizenModelFactory


class TestCitizenRepositoryCreate:
    """Testes de criação"""
    
    def test_repository_create(self, db):
        """Testa criação de cidadão"""
        repo = CitizenRepository(db)
        
        citizen = CitizenFUC(
            citizen_id=uuid4(),
            full_name="Created User"
        )
        
        result = repo.create(citizen)
        
        assert result.full_name == "Created User"


class TestCitizenRepositoryRead:
    """Testes de leitura"""
    
    def test_repository_get_by_id(self, db):
        """Testa recuperação por ID"""
        repo = CitizenRepository(db)
        citizen = CitizenModelFactory(sqlalchemy_session=db)
        db.commit()
        
        result = repo.get_by_id(citizen.citizen_id)
        
        assert result is not None
        assert result.citizen_id == citizen.citizen_id
    
    def test_repository_get_by_id_not_found(self, db):
        """Testa recuperação com ID não existente"""
        repo = CitizenRepository(db)
        
        result = repo.get_by_id(uuid4())
        
        assert result is None
    
    def test_repository_get_by_bi(self, db):
        """Testa recuperação por BI"""
        repo = CitizenRepository(db)
        citizen = CitizenModelFactory(
            sqlalchemy_session=db,
            document_number="00000001"
        )
        db.commit()
        
        result = repo.get_by_bi("00000001")
        
        assert result is not None
        assert result.document_number == "00000001"
    
    def test_repository_get_by_bi_not_found(self, db):
        """Testa recuperação com BI não existente"""
        repo = CitizenRepository(db)
        
        result = repo.get_by_bi("NONEXISTENT")
        
        assert result is None


class TestCitizenRepositoryList:
    """Testes de listagem"""
    
    def test_repository_list_all(self, db):
        """Testa listagem de todos"""
        repo = CitizenRepository(db)
        
        for i in range(3):
            CitizenModelFactory(sqlalchemy_session=db, full_name=f"User {i}")
        db.commit()
        
        result = repo.list_all()
        
        assert len(result) == 3
    
    def test_repository_list_all_pagination(self, db):
        """Testa listagem com paginação"""
        repo = CitizenRepository(db)
        
        for i in range(10):
            CitizenModelFactory(sqlalchemy_session=db)
        db.commit()
        
        page1 = repo.list_all(limit=3, offset=0)
        page2 = repo.list_all(limit=3, offset=3)
        
        assert len(page1) == 3
        assert len(page2) == 3
        assert page1[0].citizen_id != page2[0].citizen_id


class TestCitizenRepositorySearch:
    """Testes de busca"""
    
    def test_repository_search_by_name(self, db):
        """Testa busca por nome"""
        repo = CitizenRepository(db)
        
        CitizenModelFactory(sqlalchemy_session=db, full_name="João Silva")
        CitizenModelFactory(sqlalchemy_session=db, full_name="Maria Santos")
        CitizenModelFactory(sqlalchemy_session=db, full_name="Pedro Costa")
        db.commit()
        
        result = repo.search_by_name("João")
        
        assert len(result) == 1
        assert result[0].full_name == "João Silva"
    
    def test_repository_search_by_name_case_insensitive(self, db):
        """Testa busca case-insensitive"""
        repo = CitizenRepository(db)
        
        CitizenModelFactory(sqlalchemy_session=db, full_name="Test User")
        db.commit()
        
        result_lower = repo.search_by_name("test")
        result_upper = repo.search_by_name("TEST")
        
        assert len(result_lower) == 1
        assert len(result_upper) == 1
    
    def test_repository_search_by_name_partial(self, db):
        """Testa busca com match parcial"""
        repo = CitizenRepository(db)
        
        CitizenModelFactory(sqlalchemy_session=db, full_name="João Silva")
        CitizenModelFactory(sqlalchemy_session=db, full_name="João Santos")
        CitizenModelFactory(sqlalchemy_session=db, full_name="Maria Silva")
        db.commit()
        
        result = repo.search_by_name("Silva")
        
        assert len(result) == 2
        assert all("Silva" in c.full_name for c in result)
    
    def test_repository_search_no_results(self, db):
        """Testa busca sem resultados"""
        repo = CitizenRepository(db)
        
        result = repo.search_by_name("Nonexistent Name")
        
        assert result == []


class TestCitizenRepositoryUpdate:
    """Testes de atualização"""
    
    def test_repository_update(self, db):
        """Testa atualização de cidadão"""
        repo = CitizenRepository(db)
        citizen = CitizenModelFactory(
            sqlalchemy_session=db,
            phone="+244912345678"
        )
        db.commit()
        
        citizen.phone = "+244987654321"
        result = repo.update(citizen)
        
        assert result.phone == "+244987654321"
