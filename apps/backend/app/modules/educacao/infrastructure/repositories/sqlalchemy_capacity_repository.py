from __future__ import annotations

from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

# Avoid importing the port interface here to prevent circular imports during
# test collection. The concrete repository implements the port shape but does
# not inherit explicitly to keep import order safe.
from apps.backend.app.modules.educacao.infrastructure.models.institution_capacity_model import (
    InstitutionCapacityModel,
)


class SQLAlchemyCapacityRepository:
    """Repositório real para InstitutionCapacityModel com lock transacional pessimista.
    
    REGRA CRÍTICA: "Nunca confiar em: capacity_total - capacity_used sem lock transacional"
    Todas as operações de cálculo de disponibilidade DEVEM usar with_for_update().
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, capacity_data: dict) -> dict:
        """Salvar registro de capacidade com validação de UNIQUE constraint (institution_id, grade, shift)."""
        model = await self.session.get(InstitutionCapacityModel, capacity_data.get("id"))
        if not model:
            model = InstitutionCapacityModel(id=capacity_data.get("id"))
            self.session.add(model)

        model.institution_id = capacity_data.get("institution_id")
        model.grade = capacity_data.get("grade")
        model.shift = capacity_data.get("shift")
        model.capacity_total = capacity_data.get("capacity_total")
        model.capacity_used = capacity_data.get("capacity_used", 0)
        model.capacity_reserved = capacity_data.get("capacity_reserved", 0)

        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    async def get_by_id(self, id: UUID) -> dict | None:
        """Obter capacidade por UUID."""
        model = await self.session.get(InstitutionCapacityModel, id)
        return self._to_dict(model) if model else None

    async def get_by_institution_grade_shift(
        self, institution_id: UUID, grade: str, shift: str, for_update: bool = False
    ) -> dict | None:
        """Obter capacidade específica COM opção de lock pessimista.
        
        CRÍTICO: PASSO 6 - Para operações de reserva, sempre usar for_update=True
        dentro de uma transação explícita para evitar race conditions.
        
        Exemplo seguro:
            async with session.begin():
                capacity = await capacity_repo.get_by_institution_grade_shift(
                    institution_id, grade, shift, for_update=True
                )
                if capacity and capacity['available'] >= quantity:
                    # operação de reserva
        """
        stmt = select(InstitutionCapacityModel).where(
            and_(
                InstitutionCapacityModel.institution_id == institution_id,
                InstitutionCapacityModel.grade == grade,
                InstitutionCapacityModel.shift == shift,
            )
        )
        if for_update:
            stmt = stmt.with_for_update()
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_dict(model) if model else None

    async def list_capacities(self, institution_id: UUID) -> list[dict]:
        """Listar todas as capacidades de uma instituição."""
        stmt = select(InstitutionCapacityModel).where(
            InstitutionCapacityModel.institution_id == institution_id
        )
        models = (await self.session.execute(stmt)).scalars().all()
        return [self._to_dict(m) for m in models]

    async def reserve_capacity(
        self, institution_id: UUID, grade: str, shift: str, quantity: int
    ) -> dict | None:
        """Reservar vagas com lock transacional pessimista.
        
        Usa with_for_update() para garantir atomicidade:
        - Incrementa capacity_reserved
        - Valida: capacity_used + capacity_reserved <= capacity_total
        """
        stmt = (
            select(InstitutionCapacityModel)
            .where(
                and_(
                    InstitutionCapacityModel.institution_id == institution_id,
                    InstitutionCapacityModel.grade == grade,
                    InstitutionCapacityModel.shift == shift,
                )
            )
            .with_for_update()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        if not model:
            return None

        available = model.capacity_total - model.capacity_used - model.capacity_reserved
        if available < quantity:
            return None

        model.capacity_reserved += quantity
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    async def release_capacity(self, id: UUID, quantity: int) -> dict | None:
        """Liberar vagas reservadas com lock transacional pessimista.
        
        Usa with_for_update() para garantir atomicidade:
        - Decrementa capacity_reserved
        """
        stmt = select(InstitutionCapacityModel).where(InstitutionCapacityModel.id == id).with_for_update()
        model = (await self.session.execute(stmt)).scalars().first()
        if not model:
            return None

        model.capacity_reserved = max(0, model.capacity_reserved - quantity)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    async def get_available(self, institution_id: UUID, grade: str, shift: str) -> int:
        """Calcular vagas disponíveis COM lock transacional pessimista.
        
        Retorna: capacity_total - capacity_used - capacity_reserved
        DEVE ser chamado dentro de with_for_update() lock.
        """
        stmt = (
            select(InstitutionCapacityModel)
            .where(
                and_(
                    InstitutionCapacityModel.institution_id == institution_id,
                    InstitutionCapacityModel.grade == grade,
                    InstitutionCapacityModel.shift == shift,
                )
            )
            .with_for_update()
        )
        model = (await self.session.execute(stmt)).scalars().first()
        if not model:
            return 0

        return max(0, model.capacity_total - model.capacity_used - model.capacity_reserved)

    async def update_capacity_used(self, id: UUID, quantity: int) -> dict | None:
        """Incrementar capacity_used com lock pessimista (matrícula finalizada)."""
        stmt = select(InstitutionCapacityModel).where(InstitutionCapacityModel.id == id).with_for_update()
        model = (await self.session.execute(stmt)).scalars().first()
        if not model:
            return None

        model.capacity_used += quantity
        model.capacity_reserved = max(0, model.capacity_reserved - quantity)
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_dict(model)

    def _to_dict(self, model: InstitutionCapacityModel | None) -> dict | None:
        """Converter modelo SQLAlchemy para dict."""
        if not model:
            return None
        return {
            "id": model.id,
            "institution_id": model.institution_id,
            "grade": model.grade,
            "shift": model.shift,
            "capacity_total": model.capacity_total,
            "capacity_used": model.capacity_used,
            "capacity_reserved": model.capacity_reserved,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }
