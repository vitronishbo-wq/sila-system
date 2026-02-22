"""CRUD operations for education module."""

from typing import Any, Dict, List, Optional

from sqlalchemy import extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.education.models.ensino_superior import EnsinoSuperior
from modules.education.models.historico_escolar import HistoricoEscolar
from modules.education.models.matricula_escolar import MatriculaEscolar
from modules.education.schemas.education_crud import (
    EnsinoSuperiorCreate,
    EnsinoSuperiorInDB,
    EnsinoSuperiorUpdate,
    HistoricoCreate,
    HistoricoInDB,
    HistoricoUpdate,
    MatriculaCreate,
    MatriculaFilter,
    MatriculaInDB,
    MatriculaUpdate,
)


class MatriculaCRUD:
    """CRUD operations for student enrollment (Matricula Escolar)."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # Standard CRUD Operations
    async def create(self, obj_in: MatriculaCreate) -> MatriculaInDB:
        """Create a new student enrollment."""
        db_obj = MatriculaEscolar(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return MatriculaInDB.model_validate(db_obj)

    async def get(self, id: int) -> Optional[MatriculaInDB]:
        """Get enrollment by ID."""
        result = await self.db.execute(
            select(MatriculaEscolar).where(MatriculaEscolar.id == id)
        )
        obj = result.scalar_one_or_none()
        if obj:
            return MatriculaInDB.model_validate(obj)
        return None

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        school_id: Optional[int] = None,
        year: Optional[int] = None,
    ) -> List[MatriculaInDB]:
        """Get multiple enrollments with optional filtering."""
        query = select(MatriculaEscolar)

        if school_id:
            query = query.where(MatriculaEscolar.school_id == school_id)

        if year:
            query = query.where(
                extract("year", MatriculaEscolar.enrollment_date) == year
            )

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return [MatriculaInDB.model_validate(obj) for obj in result.scalars().all()]

    async def update(self, id: int, obj_in: MatriculaUpdate) -> Optional[MatriculaInDB]:
        """Update enrollment record."""
        result = await self.db.execute(
            select(MatriculaEscolar).where(MatriculaEscolar.id == id)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        await self.db.commit()
        await self.db.refresh(db_obj)
        return MatriculaInDB.model_validate(db_obj)

    async def remove(self, id: int) -> Optional[MatriculaInDB]:
        """Remove enrollment record."""
        result = await self.db.execute(
            select(MatriculaEscolar).where(MatriculaEscolar.id == id)
        )
        obj = result.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
            return MatriculaInDB.model_validate(obj)
        return None

    # Advanced Query Operations
    async def get_by_student(self, student_id: str) -> List[MatriculaInDB]:
        """Get all enrollments for a specific student."""
        result = await self.db.execute(
            select(MatriculaEscolar).where(MatriculaEscolar.student_id == student_id)
        )
        return [MatriculaInDB.model_validate(obj) for obj in result.scalars().all()]

    async def get_by_school(self, school_id: int) -> List[MatriculaInDB]:
        """Get all enrollments for a specific school."""
        result = await self.db.execute(
            select(MatriculaEscolar).where(MatriculaEscolar.school_id == school_id)
        )
        return [MatriculaInDB.model_validate(obj) for obj in result.scalars().all()]

    async def get_by_grade(self, grade: str) -> List[MatriculaInDB]:
        """Get enrollments by grade level."""
        result = await self.db.execute(
            select(MatriculaEscolar).where(MatriculaEscolar.grade == grade)
        )
        return [MatriculaInDB.model_validate(obj) for obj in result.scalars().all()]

    async def search(self, filters: MatriculaFilter) -> List[MatriculaInDB]:
        """Search enrollments with multiple filters."""
        query = select(MatriculaEscolar)

        if filters.student_id:
            query = query.where(MatriculaEscolar.student_id == filters.student_id)

        if filters.school_id:
            query = query.where(MatriculaEscolar.school_id == filters.school_id)

        if filters.grade:
            query = query.where(MatriculaEscolar.grade == filters.grade)

        if filters.status:
            query = query.where(MatriculaEscolar.status == filters.status)

        if filters.year:
            query = query.where(
                extract("year", MatriculaEscolar.enrollment_date) == filters.year
            )

        if filters.date_from:
            query = query.where(MatriculaEscolar.enrollment_date >= filters.date_from)

        if filters.date_to:
            query = query.where(MatriculaEscolar.enrollment_date <= filters.date_to)

        # Apply pagination
        if filters.skip:
            query = query.offset(filters.skip)
        if filters.limit:
            query = query.limit(filters.limit)

        result = await self.db.execute(query)
        return [MatriculaInDB.model_validate(obj) for obj in result.scalars().all()]

    # Statistics and Analytics
    async def get_enrollment_statistics(
        self, school_id: Optional[int] = None, year: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get enrollment statistics."""
        query = select(
            func.count(MatriculaEscolar.id).label("total_enrollments"),
            func.count(func.distinct(MatriculaEscolar.student_id)).label(
                "unique_students"
            ),
        )

        if school_id:
            query = query.where(MatriculaEscolar.school_id == school_id)

        if year:
            query = query.where(
                extract("year", MatriculaEscolar.enrollment_date) == year
            )

        result = await self.db.execute(query)
        stats = result.first()

        return {
            "total_enrollments": stats.total_enrollments or 0,
            "unique_students": stats.unique_students or 0,
        }

    async def get_by_grade_breakdown(
        self, school_id: Optional[int] = None
    ) -> Dict[str, int]:
        """Get enrollment breakdown by grade."""
        query = select(
            MatriculaEscolar.grade, func.count(MatriculaEscolar.id).label("count")
        ).group_by(MatriculaEscolar.grade)

        if school_id:
            query = query.where(MatriculaEscolar.school_id == school_id)

        result = await self.db.execute(query)
        breakdown = {}

        for row in result:
            breakdown[row.grade] = row.count

        return breakdown

    async def get_active_enrollments(
        self, school_id: Optional[int] = None
    ) -> List[MatriculaInDB]:
        """Get currently active enrollments."""
        query = select(MatriculaEscolar).where(MatriculaEscolar.status == "ACTIVE")

        if school_id:
            query = query.where(MatriculaEscolar.school_id == school_id)

        result = await self.db.execute(query)
        return [MatriculaInDB.model_validate(obj) for obj in result.scalars().all()]

    # Batch Operations
    async def create_batch(
        self, objects_in: List[MatriculaCreate]
    ) -> List[MatriculaInDB]:
        """Create multiple enrollments in batch."""
        db_objects = [MatriculaEscolar(**obj.model_dump()) for obj in objects_in]
        self.db.add_all(db_objects)
        await self.db.commit()

        for obj in db_objects:
            await self.db.refresh(obj)

        return [MatriculaInDB.model_validate(obj) for obj in db_objects]


class HistoricoCRUD:
    """CRUD operations for academic history (Historico Escolar)."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj_in: HistoricoCreate) -> HistoricoInDB:
        """Create new academic history record."""
        db_obj = HistoricoEscolar(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return HistoricoInDB.model_validate(db_obj)

    async def get(self, id: int) -> Optional[HistoricoInDB]:
        """Get academic history by ID."""
        result = await self.db.execute(
            select(HistoricoEscolar).where(HistoricoEscolar.id == id)
        )
        obj = result.scalar_one_or_none()
        if obj:
            return HistoricoInDB.model_validate(obj)
        return None

    async def get_by_student(self, student_id: str) -> List[HistoricoInDB]:
        """Get academic history for a specific student."""
        result = await self.db.execute(
            select(HistoricoEscolar)
            .where(HistoricoEscolar.student_id == student_id)
            .order_by(HistoricoEscolar.year.desc(), HistoricoEscolar.semester.desc())
        )
        return [HistoricoInDB.model_validate(obj) for obj in result.scalars().all()]

    async def update(self, id: int, obj_in: HistoricoUpdate) -> Optional[HistoricoInDB]:
        """Update academic history record."""
        result = await self.db.execute(
            select(HistoricoEscolar).where(HistoricoEscolar.id == id)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        await self.db.commit()
        await self.db.refresh(db_obj)
        return HistoricoInDB.model_validate(db_obj)


class EnsinoSuperiorCRUD:
    """CRUD operations for higher education (Ensino Superior)."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, obj_in: EnsinoSuperiorCreate) -> EnsinoSuperiorInDB:
        """Create new higher education record."""
        db_obj = EnsinoSuperior(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return EnsinoSuperiorInDB.model_validate(db_obj)

    async def get(self, id: int) -> Optional[EnsinoSuperiorInDB]:
        """Get higher education record by ID."""
        result = await self.db.execute(
            select(EnsinoSuperior).where(EnsinoSuperior.id == id)
        )
        obj = result.scalar_one_or_none()
        if obj:
            return EnsinoSuperiorInDB.model_validate(obj)
        return None

    async def get_by_student(self, student_id: str) -> List[EnsinoSuperiorInDB]:
        """Get higher education records for a student."""
        result = await self.db.execute(
            select(EnsinoSuperior).where(EnsinoSuperior.student_id == student_id)
        )
        return [
            EnsinoSuperiorInDB.model_validate(obj) for obj in result.scalars().all()
        ]

    async def get_by_institution(self, institution_id: int) -> List[EnsinoSuperiorInDB]:
        """Get records by educational institution."""
        result = await self.db.execute(
            select(EnsinoSuperior).where(
                EnsinoSuperior.institution_id == institution_id
            )
        )
        return [
            EnsinoSuperiorInDB.model_validate(obj) for obj in result.scalars().all()
        ]

    async def update(
        self, id: int, obj_in: EnsinoSuperiorUpdate
    ) -> Optional[EnsinoSuperiorInDB]:
        """Update higher education record."""
        result = await self.db.execute(
            select(EnsinoSuperior).where(EnsinoSuperior.id == id)
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        await self.db.commit()
        await self.db.refresh(db_obj)
        return EnsinoSuperiorInDB.model_validate(db_obj)


# Factory functions for dependency injection
def get_matricula_crud(db: AsyncSession) -> MatriculaCRUD:
    """Get enrollment CRUD instance."""
    return MatriculaCRUD(db)


def get_historico_crud(db: AsyncSession) -> HistoricoCRUD:
    """Get academic history CRUD instance."""
    return HistoricoCRUD(db)


def get_ensino_superior_crud(db: AsyncSession) -> EnsinoSuperiorCRUD:
    """Get higher education CRUD instance."""
    return EnsinoSuperiorCRUD(db)


# Main education CRUD factory
def get_education_crud(db: AsyncSession) -> Dict[str, Any]:
    """Get all education CRUD instances."""
    return {
        "matricula": get_matricula_crud(db),
        "historico": get_historico_crud(db),
        "ensino_superior": get_ensino_superior_crud(db),
    }


__all__ = [
    "MatriculaCRUD",
    "HistoricoCRUD",
    "EnsinoSuperiorCRUD",
    "get_matricula_crud",
    "get_historico_crud",
    "get_ensino_superior_crud",
    "get_education_crud",
]
