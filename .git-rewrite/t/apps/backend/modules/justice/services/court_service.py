"""Court service for the justice module."""

from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from core.logging.metrics import log_activity
from modules.justice.models import (
    Case,
    Court,
    CourtJurisdiction,
    CourtStatus,
    CourtType,
)
from modules.justice.schemas import CourtCreate, CourtUpdate


class CourtService:
    """Service for managing courts."""

    @staticmethod
    def create_court(
        db: Session, court_data: CourtCreate, current_user_id: int
    ) -> Court:
        """Create a new court."""
        try:
            # Check if court code already exists
            existing_court = (
                db.query(Court).filter(Court.code == court_data.code).first()
            )
            if existing_court:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Código do tribunal já existe",
                )
            # Validar location
            province = db.execute(
                "SELECT id FROM province WHERE id = :id", {"id": court_data.province_id}
            ).fetchone()
            if not province:
                raise HTTPException(status_code=400, detail="Província inválida")
            municipality = None
            if court_data.municipality_id:
                municipality = db.execute(
                    "SELECT id FROM municipality WHERE id = :id",
                    {"id": court_data.municipality_id},
                ).fetchone()
                if not municipality:
                    raise HTTPException(status_code=400, detail="Município inválido")
            commune = None
            if court_data.commune_id:
                commune = db.execute(
                    "SELECT id FROM commune WHERE id = :id",
                    {"id": court_data.commune_id},
                ).fetchone()
                if not commune:
                    raise HTTPException(status_code=400, detail="Comuna inválida")
            # Create court
            db_court = Court(
                name=court_data.name,
                code=court_data.code,
                court_type=court_data.court_type,
                jurisdiction=court_data.jurisdiction,
                province_id=court_data.province_id,
                municipality_id=court_data.municipality_id,
                commune_id=court_data.commune_id,
                address=court_data.address,
                postal_code=court_data.postal_code,
                phone=court_data.phone,
                email=court_data.email,
                website=court_data.website,
                chief_judge=court_data.chief_judge,
                secretary=court_data.secretary,
                total_judges=court_data.total_judges,
                courtrooms=court_data.courtrooms,
                operating_hours=court_data.operating_hours,
                languages=court_data.languages,
                specializations=court_data.specializations,
                max_cases_per_month=court_data.max_cases_per_month,
                created_by=current_user_id,
            )
            db.add(db_court)
            db.commit()
            db.refresh(db_court)
            # Log activity
            log_activity(
                user_id=current_user_id,
                action="CREATE_COURT",
                resource_type="Court",
                resource_id=db_court.id,
                details=f"Tribunal criado: {court_data.code} - {court_data.name}",
            )
            return db_court
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar tribunal: {str(e)}",
            )

    @staticmethod
    def get_court(db: Session, court_id: int) -> Optional[Court]:
        """Get a court by ID."""
        return db.query(Court).filter(Court.id == court_id).first()

    @staticmethod
    def get_court_by_code(db: Session, court_code: str) -> Optional[Court]:
        """Get a court by code."""
        return db.query(Court).filter(Court.code == court_code).first()

    @staticmethod
    def get_courts(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        court_type: Optional[CourtType] = None,
        jurisdiction: Optional[CourtJurisdiction] = None,
        province: Optional[str] = None,
        municipality: Optional[str] = None,
        status: Optional[CourtStatus] = None,
        search: Optional[str] = None,
    ) -> List[Court]:
        """Get courts with filtering options."""
        query = db.query(Court)

        # Apply filters
        if court_type:
            query = query.filter(Court.court_type == court_type)

        if jurisdiction:
            query = query.filter(Court.jurisdiction == jurisdiction)

        if province:
            query = query.filter(Court.province.ilike(f"%{province}%"))

        if municipality:
            query = query.filter(Court.municipality.ilike(f"%{municipality}%"))

        if status:
            query = query.filter(Court.status == status)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Court.name.ilike(search_term),
                    Court.code.ilike(search_term),
                    Court.address.ilike(search_term),
                    Court.chief_judge.ilike(search_term),
                )
            )

        return query.order_by(Court.name).offset(skip).limit(limit).all()

    @staticmethod
    def update_court(
        db: Session, court_id: int, court_update: CourtUpdate, current_user_id: int
    ) -> Optional[Court]:
        """Update a court."""
        court = db.query(Court).filter(Court.id == court_id).first()

        if not court:
            return None

        try:
            # Update fields
            update_data = court_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(court, field, value)

            court.updated_by = current_user_id

            db.commit()
            db.refresh(court)

            # Log activity
            log_activity(
                user_id=current_user_id,
                action="UPDATE_COURT",
                resource_type="Court",
                resource_id=court.id,
                details=f"Tribunal atualizado: {court.code}",
            )

            return court

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar tribunal: {str(e)}",
            )

    @staticmethod
    def activate_court(
        db: Session, court_id: int, current_user_id: int
    ) -> Optional[Court]:
        """Activate a court."""
        court = db.query(Court).filter(Court.id == court_id).first()

        if not court:
            return None

        if court.status == CourtStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Tribunal já está ativo"
            )

        try:
            court.status = CourtStatus.ACTIVE
            court.updated_by = current_user_id

            db.commit()
            db.refresh(court)

            # Log activity
            log_activity(
                user_id=current_user_id,
                action="ACTIVATE_COURT",
                resource_type="Court",
                resource_id=court.id,
                details=f"Tribunal ativado: {court.code}",
            )

            return court

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao ativar tribunal: {str(e)}",
            )

    @staticmethod
    def deactivate_court(
        db: Session, court_id: int, current_user_id: int, reason: Optional[str] = None
    ) -> Optional[Court]:
        """Deactivate a court."""
        court = db.query(Court).filter(Court.id == court_id).first()

        if not court:
            return None

        if court.status == CourtStatus.INACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tribunal já está inativo",
            )

        # Check for active cases
        active_cases = (
            db.query(Case)
            .filter(
                Case.court_id == court_id,
                Case.status.in_(["registered", "in_progress"]),
            )
            .count()
        )

        if active_cases > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Não é possível desativar tribunal com {active_cases} processos ativos",
            )

        try:
            court.status = CourtStatus.INACTIVE
            court.updated_by = current_user_id

            db.commit()
            db.refresh(court)

            # Log activity
            log_activity(
                user_id=current_user_id,
                action="DEACTIVATE_COURT",
                resource_type="Court",
                resource_id=court.id,
                details=f"Tribunal desativado: {court.code}. Motivo: {reason or 'Não especificado'}",
            )

            return court

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao desativar tribunal: {str(e)}",
            )

    @staticmethod
    def update_case_load(db: Session, court_id: int) -> Optional[Court]:
        """Update court's current case load based on active cases."""
        court = db.query(Court).filter(Court.id == court_id).first()

        if not court:
            return None

        # Count active cases
        active_cases = (
            db.query(Case)
            .filter(
                Case.court_id == court_id,
                Case.status.in_(["registered", "in_progress"]),
            )
            .count()
        )

        court.current_case_load = active_cases
        db.commit()
        db.refresh(court)

        return court

    @staticmethod
    def get_courts_by_province(db: Session, province: str) -> List[Court]:
        """Get all courts in a specific province."""
        return (
            db.query(Court)
            .filter(
                Court.province.ilike(f"%{province}%"),
                Court.status == CourtStatus.ACTIVE,
            )
            .order_by(Court.name)
            .all()
        )

    @staticmethod
    def get_available_courts(
        db: Session, case_type: Optional[str] = None, province: Optional[str] = None
    ) -> List[Court]:
        """Get courts available for new cases (not overloaded)."""
        query = db.query(Court).filter(Court.status == CourtStatus.ACTIVE)

        if province:
            query = query.filter(Court.province.ilike(f"%{province}%"))

        courts = query.all()

        # Filter out overloaded courts
        available_courts = []
        for court in courts:
            if not court.is_overloaded:
                available_courts.append(court)

        return sorted(available_courts, key=lambda c: c.capacity_utilization)

    @staticmethod
    def get_court_statistics(
        db: Session, court_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get court statistics."""
        if court_id:
            query = db.query(Court).filter(Court.id == court_id)
        else:
            query = db.query(Court)

        total_courts = query.count()
        active_courts = query.filter(Court.status == CourtStatus.ACTIVE).count()
        inactive_courts = query.filter(Court.status == CourtStatus.INACTIVE).count()

        # Courts by type
        courts_by_type = {}
        for court_type in CourtType:
            count = query.filter(Court.court_type == court_type).count()
            courts_by_type[court_type.value] = count

        # Courts by jurisdiction
        courts_by_jurisdiction = {}
        for jurisdiction in CourtJurisdiction:
            count = query.filter(Court.jurisdiction == jurisdiction).count()
            courts_by_jurisdiction[jurisdiction.value] = count

        # Courts by province
        courts_by_province = {}
        provinces = db.query(Court.province).distinct().all()
        for (province,) in provinces:
            if province:
                count = query.filter(Court.province == province).count()
                courts_by_province[province] = count

        # Capacity statistics
        courts = query.filter(Court.status == CourtStatus.ACTIVE).all()
        overloaded_courts = len([c for c in courts if c.is_overloaded])

        total_capacity = sum(c.max_cases_per_month or 0 for c in courts)
        total_load = sum(c.current_case_load for c in courts)

        return {
            "total_courts": total_courts,
            "active_courts": active_courts,
            "inactive_courts": inactive_courts,
            "courts_by_type": courts_by_type,
            "courts_by_jurisdiction": courts_by_jurisdiction,
            "courts_by_province": courts_by_province,
            "overloaded_courts": overloaded_courts,
            "total_capacity": total_capacity,
            "total_case_load": total_load,
            "system_utilization": (
                (total_load / total_capacity * 100) if total_capacity > 0 else 0
            ),
        }

    @staticmethod
    def get_overloaded_courts(db: Session) -> List[Court]:
        """Get courts that are overloaded."""
        courts = db.query(Court).filter(Court.status == CourtStatus.ACTIVE).all()
        return [court for court in courts if court.is_overloaded]

    @staticmethod
    def assign_case_to_court(
        db: Session, case_type: str, province: str, priority: str = "medium"
    ) -> Optional[Court]:
        """Automatically assign a case to the best available court."""
        # Get available courts in the province
        available_courts = CourtService.get_available_courts(db, case_type, province)

        if not available_courts:
            return None

        # For high priority cases, prefer courts with lower load
        if priority == "high" or priority == "urgent":
            return min(available_courts, key=lambda c: c.capacity_utilization)

        # For normal cases, use round-robin or least loaded
        return min(available_courts, key=lambda c: c.current_case_load)

    @staticmethod
    def get_court_workload_report(db: Session, court_id: int) -> Dict[str, Any]:
        """Generate detailed workload report for a court."""
        court = db.query(Court).filter(Court.id == court_id).first()

        if not court:
            return {}

        # Get case statistics
        from modules.justice.services.case_service import CaseService

        case_stats = CaseService.get_case_statistics(db, court_id)

        # Get event statistics
        from modules.justice.services.case_event_service import CaseEventService

        event_stats = CaseEventService.get_event_statistics(db, court_id)

        # Calculate efficiency metrics
        cases_per_judge = (
            case_stats["total_cases"] / court.total_judges
            if court.total_judges > 0
            else 0
        )
        cases_per_courtroom = (
            case_stats["total_cases"] / court.courtrooms if court.courtrooms > 0 else 0
        )

        return {
            "court_info": {
                "name": court.name,
                "code": court.code,
                "type": court.court_type.value,
                "judges": court.total_judges,
                "courtrooms": court.courtrooms,
                "capacity": court.max_cases_per_month,
            },
            "case_statistics": case_stats,
            "event_statistics": event_stats,
            "efficiency_metrics": {
                "cases_per_judge": cases_per_judge,
                "cases_per_courtroom": cases_per_courtroom,
                "capacity_utilization": court.capacity_utilization,
                "is_overloaded": court.is_overloaded,
            },
        }
