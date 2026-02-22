"""Service layer for justice module operations."""

import logging
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from .. import models, schemas

logger = logging.getLogger(__name__)


class CaseType:
    """Tipos de casos jurídicos."""

    CIVIL = "CIVIL"
    CRIMINAL = "CRIMINAL"
    FAMILY = "FAMILY"
    COMMERCIAL = "COMMERCIAL"
    LABOR = "LABOR"


class CaseStatus:
    """Status dos casos."""

    REGISTERED = "REGISTERED"
    IN_PROGRESS = "IN_PROGRESS"
    SUSPENDED = "SUSPENDED"
    CONCLUDED = "CONCLUDED"
    ARCHIVED = "ARCHIVED"


class CasePriority:
    """Prioridades dos casos."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class JusticeService:
    """Service class for justice operations."""

    # Valor máximo para causas (para evitar custas excessivas)
    MAX_CAUSE_VALUE = Decimal("10000000.00")  # 10 milhões

    # Prazos em dias
    CIVIL_DEADLINE = 15
    CRIMINAL_DEADLINE = 5
    FAMILY_DEADLINE = 10
    COMMERCIAL_DEADLINE = 20
    LABOR_DEADLINE = 8

    # Prazo para apelação (dias)
    APPEAL_DEADLINE = 15

    @staticmethod
    def create_certificate(
        db: Session, certificate: schemas.JudicialCertificateCreate
    ) -> models.JudicialCertificate:
        """Create a new judicial certificate."""
        db_certificate = models.JudicialCertificate(
            citizen_id=certificate.citizen_id,
            type=certificate.type,
            status=certificate.status,
            notes=certificate.notes,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(db_certificate)
        db.commit()
        db.refresh(db_certificate)
        return db_certificate

    async def create_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new legal case."""
        # Validação dos dados
        if not await self.validate_case_data(case_data):
            raise ValueError("Dados do caso inválidos")

        # Simulação de criação
        case = {
            "id": 1,
            **case_data,
            "created_at": datetime.now(timezone.utc),
            "status": CaseStatus.REGISTERED,
        }

        logger.info(f"Caso jurídico criado: {case['numero_processo']}")
        return case

    async def validate_case_data(self, case_data: Dict[str, Any]) -> bool:
        """Validate legal case data."""
        try:
            # Verifica número de processo
            process_number = case_data.get("numero_processo", "")
            if not self._validate_process_number(process_number):
                return False

            # Verifica valor da causa
            cause_value = case_data.get("valor_causa", Decimal("0"))
            if cause_value < 0 or cause_value > self.MAX_CAUSE_VALUE:
                return False

            # Verifica data de abertura
            opening_date = case_data.get("data_abertura")
            if opening_date and isinstance(opening_date, datetime):
                if opening_date > datetime.now(timezone.utc):
                    return False

            return True

        except Exception as e:
            logger.error(f"Erro na validação: {str(e)}")
            return False

    def _validate_process_number(self, process_number: str) -> bool:
        """Validate Brazilian legal process number format."""
        # Formato: NNNNNNNN-DD.AAAA.J.TR.OOOO
        import re

        pattern = r"^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$"
        return bool(re.match(pattern, process_number))

    async def update_case_status(self, case_id: int, new_status: str) -> bool:
        """Update case status with business rules."""
        # Validação do status
        valid_statuses = [
            CaseStatus.REGISTERED,
            CaseStatus.IN_PROGRESS,
            CaseStatus.SUSPENDED,
            CaseStatus.CONCLUDED,
            CaseStatus.ARCHIVED,
        ]

        if new_status not in valid_statuses:
            return False

        # Simulação de busca no DB
        if case_id != 1:  # Simula caso não encontrado
            return False

        # Regra de negócio: não pode voltar para REGISTERED
        current_status = CaseStatus.CONCLUDED  # Simulação
        if (
            current_status == CaseStatus.ARCHIVED
            and new_status == CaseStatus.REGISTERED
        ):
            return False

        logger.info(f"Status do caso {case_id} atualizado para {new_status}")
        return True

    async def calculate_court_fees(self, case_data: Dict[str, Any]) -> Decimal:
        """Calculate court fees based on case type and value."""
        case_type = case_data.get("tipo_caso", "")
        cause_value = case_data.get("valor_causa", Decimal("0"))

        # Percentuais baseados no tipo
        fee_percentages = {
            CaseType.CIVIL: Decimal("0.01"),  # 1%
            CaseType.CRIMINAL: Decimal("0.005"),  # 0.5%
            CaseType.FAMILY: Decimal("0.005"),  # 0.5% (assistência judiciária)
            CaseType.COMMERCIAL: Decimal("0.015"),  # 1.5%
            CaseType.LABOR: Decimal("0.002"),  # 0.2%
        }

        percentage = fee_percentages.get(case_type, Decimal("0.01"))
        fees = cause_value * percentage

        # Teto máximo para custas
        max_fees = Decimal("50000.00")
        if fees > max_fees:
            fees = max_fees

        # Valor mínimo
        min_fees = Decimal("100.00")
        if fees < min_fees and cause_value > 0:
            fees = min_fees

        return fees

    async def calculate_case_deadline(self, case_data: Dict[str, Any]) -> datetime:
        """Calculate deadline based on case type."""
        case_type = case_data.get("tipo_caso", "")
        opening_date = case_data.get("data_abertura", datetime.now(timezone.utc))

        deadlines = {
            CaseType.CIVIL: self.CIVIL_DEADLINE,
            CaseType.CRIMINAL: self.CRIMINAL_DEADLINE,
            CaseType.FAMILY: self.FAMILY_DEADLINE,
            CaseType.COMMERCIAL: self.COMMERCIAL_DEADLINE,
            CaseType.LABOR: self.LABOR_DEADLINE,
        }

        days = deadlines.get(case_type, self.CIVIL_DEADLINE)
        deadline = opening_date + timedelta(days=days)

        return deadline

    async def check_case_overdue(self, case: Dict[str, Any]) -> bool:
        """Check if case is overdue."""
        deadline = case.get("prazo_limite")
        if not deadline:
            return False

        return datetime.now(timezone.utc) > deadline

    async def assign_lawyer_to_case(self, case_id: int, lawyer_id: str) -> bool:
        """Assign lawyer to case."""
        # Simulação de busca no DB
        if case_id != 1:  # Simula caso não encontrado
            return False

        # Simula verificação se já tem advogado
        current_lawyer = None  # Simulação

        if current_lawyer:
            return False  # Já tem advogado

        logger.info(f"Advogado {lawyer_id} atribuído ao caso {case_id}")
        return True

    async def get_case_statistics(self) -> Dict[str, Any]:
        """Get case statistics."""
        # Simulação de estatísticas
        return {
            "total_cases": 100,
            "cases_by_status": {"REGISTERED": 30, "IN_PROGRESS": 50, "CONCLUDED": 20},
            "cases_by_type": {
                "CIVIL": 40,
                "CRIMINAL": 25,
                "FAMILY": 20,
                "COMMERCIAL": 10,
                "LABOR": 5,
            },
        }

    async def can_appeal_case(self, case: Dict[str, Any]) -> bool:
        """Check if case can be appealed."""
        status = case.get("status")
        conclusion_date = case.get("data_conclusao")

        if status != CaseStatus.CONCLUDED:
            return False

        if not conclusion_date:
            return False

        # Verifica prazo para apelação
        days_since_conclusion = (datetime.now(timezone.utc) - conclusion_date).days
        return days_since_conclusion <= self.APPEAL_DEADLINE

    async def calculate_case_complexity(self, case_data: Dict[str, Any]) -> str:
        """Calculate case complexity."""
        case_type = case_data.get("tipo_caso", "")
        cause_value = case_data.get("valor_causa", Decimal("0"))
        num_parties = case_data.get("numero_partes", 2)
        has_witnesses = case_data.get("tem_testemunhas", False)
        has_expertise = case_data.get("tem_pericias", False)

        complexity_score = 0

        # Tipo do caso
        if case_type == CaseType.COMMERCIAL:
            complexity_score += 2
        elif case_type == CaseType.CIVIL:
            complexity_score += 1

        # Valor da causa
        if cause_value > Decimal("100000.00"):
            complexity_score += 2
        elif cause_value > Decimal("10000.00"):
            complexity_score += 1

        # Número de partes
        if num_parties > 4:
            complexity_score += 2
        elif num_parties > 2:
            complexity_score += 1

        # Testemunhas e perícias
        if has_witnesses:
            complexity_score += 1
        if has_expertise:
            complexity_score += 2

        # Classificação final
        if complexity_score >= 6:
            return "COMPLEXO"
        elif complexity_score >= 3:
            return "MÉDIO"
        else:
            return "SIMPLES"

    async def generate_case_report(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """Generate case report for date range."""
        # Simulação de relatório
        return {
            "period": f"{start_date.date()} a {end_date.date()}",
            "total_cases": 3,
            "cases_by_type": {"CIVIL": 2, "CRIMINAL": 1},
            "success_rate": 2 / 3,
            "average_duration": "45 dias",
        }

    @staticmethod
    def update_certificate(
        db: Session,
        db_certificate: models.JudicialCertificate,
        certificate_update: schemas.JudicialCertificateUpdate,
    ) -> models.JudicialCertificate:
        """Update a judicial certificate."""
        update_data = certificate_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_certificate, field, value)

        db_certificate.updated_at = datetime.utcnow()
        db.add(db_certificate)
        db.commit()
        db.refresh(db_certificate)
        return db_certificate

    @staticmethod
    def delete_certificate(db: Session, certificate_id: int) -> bool:
        """Delete a judicial certificate."""
        db_certificate = JusticeService.get_certificate(db, certificate_id)
        if db_certificate is None:
            return False

        db.delete(db_certificate)
        db.commit()
        return True


# Backward compatibility: expose functions as module-level functions
def create_certificate(
    db: Session, certificate: schemas.JudicialCertificateCreate
) -> models.JudicialCertificate:
    return JusticeService.create_certificate(db, certificate)


def get_certificate(
    db: Session, certificate_id: int
) -> Optional[models.JudicialCertificate]:
    return JusticeService.get_certificate(db, certificate_id)


def get_certificates(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    citizen_id: Optional[int] = None,
    status: Optional[schemas.CertificateStatus] = None,
) -> List[models.JudicialCertificate]:
    return JusticeService.get_certificates(db, skip, limit, citizen_id, status)


def update_certificate(
    db: Session,
    db_certificate: models.JudicialCertificate,
    certificate_update: schemas.JudicialCertificateUpdate,
) -> models.JudicialCertificate:
    return JusticeService.update_certificate(db, db_certificate, certificate_update)


def delete_certificate(db: Session, certificate_id: int) -> bool:
    return JusticeService.delete_certificate(db, certificate_id)
