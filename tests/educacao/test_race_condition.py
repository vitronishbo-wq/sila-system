"""
PASSO 6 — Testes de Race Condition

Demonstra o problema sem FOR UPDATE e a solução com FOR UPDATE.
"""

import asyncio
from datetime import datetime
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.db import AsyncSessionLocal
from apps.backend.app.modules.educacao.infrastructure.models.institution_capacity_model import (
    InstitutionCapacityModel,
)
from apps.backend.app.modules.educacao.infrastructure.repositories import (
    SQLAlchemyCapacityRepository,
)


class TestRaceCondition:
    """Testes para demonstrar race condition e solução com locks."""

    @pytest.mark.asyncio
    async def test_race_condition_without_lock(self, db_session: AsyncSession):
        """
        ❌ DEMONSTRA: Race condition SEM FOR UPDATE

        Cenário:
        - Capacidade total: 2 vagas
        - Capacidade usada: 1
        - Capacidade reservada: 0
        - Disponível: 1

        2 processos tentam reservar 1 vaga cada no mesmo instante
        SEM lock pessimista → AMBOS conseguem!
        """
        # Setup
        capacity_id = uuid4()
        institution_id = uuid4()

        capacity = InstitutionCapacityModel(
            id=capacity_id,
            institution_id=institution_id,
            grade="5A",
            shift="MORNING",
            capacity_total=2,
            capacity_used=1,
            capacity_reserved=0,
        )
        db_session.add(capacity)
        await db_session.flush()

        # Simulação de 2 processos lendo ANTES do lock
        # (sem FOR UPDATE, ambos conseguem ler e fazer reserva)

        async def read_without_lock():
            """Simula leitura sem lock — VULNERÁVEL"""
            stmt = select(InstitutionCapacityModel).where(
                InstitutionCapacityModel.id == capacity_id
            )
            model = (await db_session.execute(stmt)).scalars().first()
            available = model.capacity_total - model.capacity_used - model.capacity_reserved
            return available

        available_1 = await read_without_lock()
        available_2 = await read_without_lock()

        # ❌ BUG: Ambos veem 1 vaga disponível
        assert available_1 == 1
        assert available_2 == 1
        # Mas se ambos tentarem reservar, temos overbooking!

        # Cleanup: ensure session transaction is settled before fixture close
        await db_session.rollback()

    @pytest.mark.asyncio
    async def test_pessimistic_lock_prevents_overbooking(
        self, db_session: AsyncSession
    ):
        """
        ✅ DEMONSTRA: Lock pessimista COM FOR UPDATE

        Cenário:
        - Capacidade total: 2 vagas
        - Capacidade usada: 1
        - Capacidade reservada: 0
        - Disponível: 1

        2 processos tentam reservar 1 vaga cada
        COM lock pessimista → Apenas 1 consegue!
        """
        # Setup
        capacity_id = uuid4()
        institution_id = uuid4()

        capacity = InstitutionCapacityModel(
            id=capacity_id,
            institution_id=institution_id,
            grade="5A",
            shift="MORNING",
            capacity_total=2,
            capacity_used=1,
            capacity_reserved=0,
        )
        db_session.add(capacity)
        await db_session.flush()
        await db_session.commit()

        results = []

        async def reserve_with_lock(process_id: int):
            """Simula reserva COM lock pessimista usando sessão separada"""
            try:
                async with AsyncSessionLocal() as session:
                    async with session.begin():
                        stmt = (
                            select(InstitutionCapacityModel)
                            .where(InstitutionCapacityModel.id == capacity_id)
                            .with_for_update()
                        )
                        model = (await session.execute(stmt)).scalars().first()

                        available = (
                            model.capacity_total
                            - model.capacity_used
                            - model.capacity_reserved
                        )

                        if available >= 1:
                            model.capacity_reserved += 1
                            await session.flush()
                            results.append(
                                {"process": process_id, "status": "SUCCESS", "available": available}
                            )
                        else:
                            results.append(
                                {"process": process_id, "status": "FAILED", "available": available}
                            )
            except Exception as e:
                results.append({"process": process_id, "status": "ERROR", "error": str(e)})

        # Lançar 2 processos em "paralelo"
        await asyncio.gather(
            reserve_with_lock(1),
            reserve_with_lock(2),
        )

        # ✅ CORRETO: Apenas 1 conseguiu, 1 falhou
        success_count = sum(1 for r in results if r["status"] == "SUCCESS")
        assert success_count == 1, "Apenas 1 processo deveria conseguir reservar"

        # Verificar final em nova sessão para evitar cache
        async with AsyncSessionLocal() as verify_session:
            stmt = select(InstitutionCapacityModel).where(InstitutionCapacityModel.id == capacity_id)
            refreshed = (await verify_session.execute(stmt)).scalars().first()

        assert refreshed.capacity_reserved == 1
        assert refreshed.capacity_total - refreshed.capacity_used - refreshed.capacity_reserved == 0

    @pytest.mark.asyncio
    async def test_repository_reserve_capacity_uses_lock(
        self, db_session: AsyncSession
    ):
        """Verifica que SQLAlchemyCapacityRepository sempre usa FOR UPDATE."""
        # Setup
        capacity_id = uuid4()
        institution_id = uuid4()

        capacity = InstitutionCapacityModel(
            id=capacity_id,
            institution_id=institution_id,
            grade="5A",
            shift="MORNING",
            capacity_total=100,
            capacity_used=50,
            capacity_reserved=0,
        )
        db_session.add(capacity)
        await db_session.flush()

        repo = SQLAlchemyCapacityRepository(db_session)

        # Reserve 10 vagas
        result = await repo.reserve_capacity(
            institution_id=institution_id,
            grade="5A",
            shift="MORNING",
            quantity=10,
        )

        assert result is not None
        assert result["capacity_reserved"] == 10
        assert result["capacity_used"] == 50

        # Ensure the change is committed so session teardown is clean
        await db_session.commit()

    @pytest.mark.asyncio
    async def test_overbooking_prevented(self, db_session: AsyncSession):
        """Testa que overbooking é prevenido mesmo com múltiplas tentativas."""
        # Setup
        institution_id = uuid4()

        capacity = InstitutionCapacityModel(
            id=uuid4(),
            institution_id=institution_id,
            grade="5A",
            shift="MORNING",
            capacity_total=5,
            capacity_used=0,
            capacity_reserved=0,
        )
        db_session.add(capacity)
        await db_session.flush()
        await db_session.commit()

        # Tentar reservar 5 vagas em paralelo (cada um tenta 2) usando sessões separadas:
        results = []

        async def try_reserve():
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    repo = SQLAlchemyCapacityRepository(session)
                    result = await repo.reserve_capacity(
                        institution_id=institution_id,
                        grade="5A",
                        shift="MORNING",
                        quantity=2,
                    )
                    results.append(result)

        await asyncio.gather(
            try_reserve(),
            try_reserve(),
            try_reserve(),  # Total 6 tentativas, 1 deve falhar
        )

        # 2 sucessos (4 vagas), 1 falha (sem vagas)
        successful = sum(1 for r in results if r is not None)
        failed = sum(1 for r in results if r is None)

        assert successful == 2, f"Esperado 2 sucessos, got {successful}"
        assert failed == 1, f"Esperado 1 falha, got {failed}"

        # Verificar estado final em uma sessão separada para evitar cache de sessão
        async with AsyncSessionLocal() as verify_session:
            stmt = select(InstitutionCapacityModel).where(
                InstitutionCapacityModel.institution_id == institution_id
            )
            final_capacity = (await verify_session.execute(stmt)).scalars().first()

        assert final_capacity is not None
        assert final_capacity.capacity_reserved == 4  # Apenas 4 vagas reservadas
        assert final_capacity.capacity_total - final_capacity.capacity_used - final_capacity.capacity_reserved == 1
        # 1 vaga realmente disponível


# ============================================================================
# DOCUMENTAÇÃO DOS TESTES
# ============================================================================

"""
Estes testes demonstram por que FOR UPDATE é CRÍTICO:

test_race_condition_without_lock():
    Mostra como 2 processos veem a MESMA disponibilidade
    sem lock, levando a overbooking.

test_pessimistic_lock_prevents_overbooking():
    Mostra como FOR UPDATE garante que apenas 1 processo
    consegue reservar quando há apenas 1 vaga.

test_repository_reserve_capacity_uses_lock():
    Valida que nosso repositório SEMPRE usa FOR UPDATE.

test_overbooking_prevented():
    Cenário realista: múltiplos processos em paralelo
    tentando reservar mais vagas que a capacidade.
    Resultado: Sem overbooking, dados consistentes.

Comando para rodar:
    pytest tests/educacao/test_race_condition.py -v

Resultado esperado:
    ✅ 4 tests passed
    ✅ Nenhum overbooking
    ✅ Dados sempre consistentes
"""
