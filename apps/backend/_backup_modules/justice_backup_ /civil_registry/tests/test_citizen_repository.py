"""
Testes de Integração para CitizenRepository
"""
import pytest
from uuid import uuid4
from datetime import date
from app.modules.justice.bounded_contexts.infrastructure.repositories.citizen_repository import CitizenRepository
from app.core.bridges.identity_bridge import CitizenFUC

@pytest.mark.asyncio
@pytest.mark.integration
class TestCitizenRepository:
    """Testes para o repositório de Cidadãos."""

    async def test_repository_create(self, async_db_session):
        """Testa criação de um cidadão."""
        repo = CitizenRepository(async_db_session)
        citizen = CitizenFUC(citizen_id=uuid4(), full_name='Test Citizen', document_number='12345678', birth_date=date(2000, 1, 1))
        result = await repo.create(citizen)
        assert result.citizen_id == citizen.citizen_id
        assert result.full_name == 'Test Citizen'

    async def test_repository_get_by_id(self, async_db_session, sample_citizen_model):
        """Testa recuperação de cidadão por ID."""
        repo = CitizenRepository(async_db_session)
        async_db_session.add(sample_citizen_model)
        await async_db_session.commit()
        result = await repo.get_by_id(sample_citizen_model.citizen_id)
        assert result is not None
        assert result.citizen_id == sample_citizen_model.citizen_id
        assert result.full_name == sample_citizen_model.full_name

    async def test_repository_get_by_id_not_found(self, async_db_session):
        """Testa recuperação com ID não existente."""
        repo = CitizenRepository(async_db_session)
        result = await repo.get_by_id(uuid4())
        assert result is None

    async def test_repository_get_by_bi(self, async_db_session, sample_citizen_model):
        """Testa recuperação de cidadão por número de BI."""
        repo = CitizenRepository(async_db_session)
        async_db_session.add(sample_citizen_model)
        await async_db_session.commit()
        result = await repo.get_by_bi(sample_citizen_model.document_number)
        assert result is not None
        assert result.document_number == sample_citizen_model.document_number

    async def test_repository_get_by_bi_not_found(self, async_db_session):
        """Testa recuperação com BI não existente."""
        repo = CitizenRepository(async_db_session)
        result = await repo.get_by_bi('NONEXISTENT')
        assert result is None

    async def test_repository_list_all(self, async_db_session):
        """Testa listagem de todos os cidadãos."""
        repo = CitizenRepository(async_db_session)
        for i in range(3):
            citizen = CitizenFUC(citizen_id=uuid4(), full_name=f'Citizen {i}')
            async_db_session.add(citizen)
        await async_db_session.commit()
        result = await repo.list_all(limit=10)
        assert len(result) == 3

    async def test_repository_list_all_with_pagination(self, async_db_session):
        """Testa listagem com paginação."""
        repo = CitizenRepository(async_db_session)
        for i in range(10):
            citizen = CitizenFUC(citizen_id=uuid4(), full_name=f'Citizen {i}')
            async_db_session.add(citizen)
        await async_db_session.commit()
        page1 = await repo.list_all(limit=3, offset=0)
        assert len(page1) == 3
        page2 = await repo.list_all(limit=3, offset=3)
        assert len(page2) == 3
        assert page1[0].citizen_id != page2[0].citizen_id

    async def test_repository_search_by_name(self, async_db_session):
        """Testa busca por nome."""
        repo = CitizenRepository(async_db_session)
        names = ['João Silva', 'Maria Santos', 'Pedro Costa']
        for name in names:
            citizen = CitizenFUC(citizen_id=uuid4(), full_name=name)
            async_db_session.add(citizen)
        await async_db_session.commit()
        result = await repo.search_by_name('João')
        assert len(result) == 1
        assert result[0].full_name == 'João Silva'

    async def test_repository_search_by_name_case_insensitive(self, async_db_session):
        """Testa busca por nome case-insensitive."""
        repo = CitizenRepository(async_db_session)
        citizen = CitizenFUC(citizen_id=uuid4(), full_name='Test User')
        async_db_session.add(citizen)
        await async_db_session.commit()
        result1 = await repo.search_by_name('test')
        result2 = await repo.search_by_name('TEST')
        result3 = await repo.search_by_name('Test')
        assert len(result1) == 1
        assert len(result2) == 1
        assert len(result3) == 1

    async def test_repository_search_by_name_partial_match(self, async_db_session):
        """Testa busca com match parcial."""
        repo = CitizenRepository(async_db_session)
        citizens_data = ['João Silva', 'João Santos', 'João Costa', 'Maria Silva']
        for name in citizens_data:
            citizen = CitizenFUC(citizen_id=uuid4(), full_name=name)
            async_db_session.add(citizen)
        await async_db_session.commit()
        result = await repo.search_by_name('Silva')
        assert len(result) == 2
        assert all(('Silva' in c.full_name for c in result))

    async def test_repository_update(self, async_db_session, sample_citizen_model):
        """Testa atualização de cidadão."""
        repo = CitizenRepository(async_db_session)
        async_db_session.add(sample_citizen_model)
        await async_db_session.commit()
        sample_citizen_model.phone = '+244999999999'
        result = await repo.update(sample_citizen_model)
        assert result.phone == '+244999999999'

@pytest.mark.asyncio
@pytest.mark.integration
class TestCitizenRepositoryEdgeCases:
    """Testes de casos extremos para CitizenRepository."""

    async def test_repository_with_empty_database(self, async_db_session):
        """Testa operações com banco vazio."""
        repo = CitizenRepository(async_db_session)
        result = await repo.list_all()
        assert result == []

    async def test_repository_search_empty_result(self, async_db_session):
        """Testa busca que não retorna resultados."""
        repo = CitizenRepository(async_db_session)
        result = await repo.search_by_name('Nonexistent Name')
        assert result == []

    async def test_repository_search_limit(self, async_db_session):
        """Testa limite de resultados em busca."""
        repo = CitizenRepository(async_db_session)
        for i in range(100):
            citizen = CitizenFUC(citizen_id=uuid4(), full_name=f'João Silva {i}')
            async_db_session.add(citizen)
        await async_db_session.commit()
        result = await repo.search_by_name('João', limit=10)
        assert len(result) == 10

    async def test_repository_duplicate_document_number(self, async_db_session):
        """Testa constraint de uniqueness em document_number."""
        repo = CitizenRepository(async_db_session)
        doc_number = 'DUPLICATE123'
        citizen1 = CitizenFUC(citizen_id=uuid4(), full_name='First', document_number=doc_number)
        citizen2 = CitizenFUC(citizen_id=uuid4(), full_name='Second', document_number=doc_number)
        async_db_session.add(citizen1)
        await async_db_session.commit()
        async_db_session.add(citizen2)
        with pytest.raises(Exception):
            await async_db_session.commit()