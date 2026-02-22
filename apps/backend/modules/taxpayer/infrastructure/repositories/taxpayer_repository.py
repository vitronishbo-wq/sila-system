"""Taxpayer Repository Implementation - DDD Aggregate Root Repository

Following DDD principles:
- Repository ONLY for Aggregate Roots
- Taxpayer = Aggregate Root
- Declarations, Debts, Payments, Certificates = Child Entities

ALL operations on child entities go through TaxpayerRepository
to maintain aggregate consistency and transactional integrity.

No separate repositories for child entities.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, extract
from datetime import datetime

from ..db.models import (
    TaxpayerModel,
    TaxDeclarationModel,
    TaxDebtModel,
    TaxPaymentModel,
    TaxCertificateModel,
)
from .base_repository import BaseRepository


class TaxpayerRepository(BaseRepository[TaxpayerModel]):
    """
    Unified Repository for Taxpayer Aggregate.
    
    Handles ALL operations on:
    - Taxpayer entity
    - Declarations (child)
    - Debts (child)
    - Payments (child)
    - Certificates (child)
    
    Maintains aggregate consistency and transactional integrity.
    """
    
    def __init__(self, db: Session):
        super().__init__(db, TaxpayerModel)
    
    # ============ TAXPAYER ROOT AGGREG ate OPERATIONS ============
    
    def save(self, taxpayer_data: dict) -> TaxpayerModel:
        """Save a taxpayer"""
        existing = self.get_by_id(taxpayer_data.get('id'))
        if existing:
            for key, value in taxpayer_data.items():
                if value is not None:
                    setattr(existing, key, value)
            self.db.flush()
            return existing
        else:
            return self.create(**taxpayer_data)
    
    def find_by_nif(self, nif: str) -> Optional[TaxpayerModel]:
        """Find taxpayer by NIF - unique lookup"""
        return self.db.query(TaxpayerModel).filter(
            TaxpayerModel.nif == nif
        ).first()
    
    def find_by_email(self, email: str) -> Optional[TaxpayerModel]:
        """Find taxpayer by email"""
        return self.db.query(TaxpayerModel).filter(
            TaxpayerModel.email == email
        ).first()
    
    def find_by_phone(self, phone: str) -> Optional[TaxpayerModel]:
        """Find taxpayer by phone"""
        return self.db.query(TaxpayerModel).filter(
            TaxpayerModel.phone == phone
        ).first()
    
    def list_all(self, skip: int = 0, limit: int = 100, filters: dict = None) -> tuple:
        """List all taxpayers"""
        models, total = self.get_all(skip, limit, "registered_at", True, filters)
        return models, total
    
    def update_status(self, taxpayer_id: UUID, status: str, updated_by: UUID) -> Optional[TaxpayerModel]:
        """Update taxpayer status"""
        return self.update(taxpayer_id, status=status, updated_by=updated_by, updated_at=datetime.now())
    
    def find_by_status(self, status: str, skip: int = 0, limit: int = 100) -> tuple:
        """Find taxpayers by status"""
        query = self.db.query(TaxpayerModel).filter(TaxpayerModel.status == status)
        total = query.count()
        models = query.order_by(desc(TaxpayerModel.registered_at)).offset(skip).limit(limit).all()
        return models, total
    
    def find_by_regime(self, tax_regime: str, skip: int = 0, limit: int = 100) -> tuple:
        """Find taxpayers by tax regime"""
        query = self.db.query(TaxpayerModel).filter(TaxpayerModel.tax_regime == tax_regime)
        total = query.count()
        models = query.offset(skip).limit(limit).all()
        return models, total
    
    def search(self, query_str: str, skip: int = 0, limit: int = 100) -> tuple:
        """Search taxpayers by NIF, name, or email"""
        query = self.db.query(TaxpayerModel).filter(
            or_(
                TaxpayerModel.nif.ilike(f"%{query_str}%"),
                TaxpayerModel.name.ilike(f"%{query_str}%"),
                TaxpayerModel.email.ilike(f"%{query_str}%")
            )
        )
        total = query.count()
        models = query.offset(skip).limit(limit).all()
        return models, total
    
    # ============ DECLARATION CHILD ENTITY OPERATIONS ============
    
    def get_declarations(
        self,
        taxpayer_id: UUID,
        year: Optional[int] = None,
        tax_type: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[TaxDeclarationModel]:
        """Get declarations for taxpayer (aggregate child operations)"""
        query = self.db.query(TaxDeclarationModel).filter(
            TaxDeclarationModel.taxpayer_id == taxpayer_id
        )
        
        if year:
            query = query.filter(extract('year', TaxDeclarationModel.due_date) == year)
        if tax_type:
            query = query.filter(TaxDeclarationModel.tax_type == tax_type)
        if status:
            query = query.filter(TaxDeclarationModel.status == status)
        
        return query.order_by(desc(TaxDeclarationModel.created_at)).limit(limit).all()
    
    def get_pending_declarations(self, taxpayer_id: UUID) -> List[TaxDeclarationModel]:
        """Get pending declarations for taxpayer"""
        return self.db.query(TaxDeclarationModel).filter(
            and_(
                TaxDeclarationModel.taxpayer_id == taxpayer_id,
                TaxDeclarationModel.status == 'PENDING'
            )
        ).order_by(TaxDeclarationModel.due_date).all()
    
    def create_declaration(
        self,
        taxpayer_id: UUID,
        **declaration_data
    ) -> TaxDeclarationModel:
        """Create declaration for taxpayer"""
        declaration = TaxDeclarationModel(
            taxpayer_id=taxpayer_id,
            **declaration_data
        )
        self.db.add(declaration)
        self.db.flush()
        return declaration
    
    # ============ DEBT CHILD ENTITY OPERATIONS ============
    
    def get_debts(
        self,
        taxpayer_id: UUID,
        include_paid: bool = False,
        tax_type: Optional[str] = None,
        limit: int = 100
    ) -> List[TaxDebtModel]:
        """Get debts for taxpayer (aggregate child operations)"""
        query = self.db.query(TaxDebtModel).filter(
            TaxDebtModel.taxpayer_id == taxpayer_id
        )
        
        if not include_paid:
            query = query.filter(TaxDebtModel.status.in_(['PENDING', 'PARTIAL']))
        if tax_type:
            query = query.filter(TaxDebtModel.tax_type == tax_type)
        
        return query.order_by(desc(TaxDebtModel.due_date)).limit(limit).all()
    
    def get_overdue_debts(self, taxpayer_id: UUID) -> List[TaxDebtModel]:
        """Get overdue debts for taxpayer"""
        now = datetime.now()
        return self.db.query(TaxDebtModel).filter(
            and_(
                TaxDebtModel.taxpayer_id == taxpayer_id,
                TaxDebtModel.due_date < now,
                TaxDebtModel.status.in_(['PENDING', 'PARTIAL'])
            )
        ).order_by(TaxDebtModel.due_date).all()
    
    def get_total_debt(self, taxpayer_id: UUID) -> float:
        """Get total outstanding debt"""
        debts = self.db.query(TaxDebtModel).filter(
            and_(
                TaxDebtModel.taxpayer_id == taxpayer_id,
                TaxDebtModel.status.in_(['PENDING', 'PARTIAL'])
            )
        ).all()
        return sum(float(d.current_amount) for d in debts)
    
    def create_debt(
        self,
        taxpayer_id: UUID,
        **debt_data
    ) -> TaxDebtModel:
        """Create debt for taxpayer"""
        debt = TaxDebtModel(
            taxpayer_id=taxpayer_id,
            **debt_data
        )
        self.db.add(debt)
        self.db.flush()
        return debt
    
    def update_debt_after_payment(
        self,
        debt_id: UUID,
        payment_amount: float
    ) -> TaxDebtModel:
        """Update debt balance after payment"""
        debt = self.db.query(TaxDebtModel).filter(TaxDebtModel.id == debt_id).first()
        if debt:
            debt.current_amount = max(0, debt.current_amount - payment_amount)
            debt.status = 'PAID' if debt.current_amount <= 0 else 'PARTIAL'
            self.db.flush()
        return debt
    
    # ============ PAYMENT CHILD ENTITY OPERATIONS ============
    
    def get_payments(
        self,
        taxpayer_id: UUID,
        year: Optional[int] = None,
        method: Optional[str] = None,
        limit: int = 100
    ) -> List[TaxPaymentModel]:
        """Get payments for taxpayer (aggregate child operations)"""
        query = self.db.query(TaxPaymentModel).filter(
            TaxPaymentModel.taxpayer_id == taxpayer_id
        )
        
        if year:
            query = query.filter(extract('year', TaxPaymentModel.payment_date) == year)
        if method:
            query = query.filter(TaxPaymentModel.payment_method == method)
        
        return query.order_by(desc(TaxPaymentModel.payment_date)).limit(limit).all()
    
    def get_total_paid(
        self,
        taxpayer_id: UUID,
        year: Optional[int] = None
    ) -> float:
        """Get total amount paid by taxpayer"""
        query = self.db.query(TaxPaymentModel).filter(
            and_(
                TaxPaymentModel.taxpayer_id == taxpayer_id,
                TaxPaymentModel.status == 'COMPLETED'
            )
        )
        
        if year:
            query = query.filter(extract('year', TaxPaymentModel.payment_date) == year)
        
        payments = query.all()
        return sum(float(p.amount) for p in payments)
    
    def create_payment(
        self,
        taxpayer_id: UUID,
        **payment_data
    ) -> TaxPaymentModel:
        """Create payment for taxpayer"""
        payment = TaxPaymentModel(
            taxpayer_id=taxpayer_id,
            **payment_data
        )
        self.db.add(payment)
        self.db.flush()
        return payment
    
    # ============ CERTIFICATE CHILD ENTITY OPERATIONS ============
    
    def get_certificates(
        self,
        taxpayer_id: UUID,
        cert_type: Optional[str] = None,
        year: Optional[int] = None,
        limit: int = 100
    ) -> List[TaxCertificateModel]:
        """Get certificates for taxpayer (aggregate child operations)"""
        query = self.db.query(TaxCertificateModel).filter(
            TaxCertificateModel.taxpayer_id == taxpayer_id
        )
        
        if cert_type:
            query = query.filter(TaxCertificateModel.certificate_type == cert_type)
        if year:
            query = query.filter(TaxCertificateModel.year == year)
        
        return query.order_by(desc(TaxCertificateModel.created_at)).limit(limit).all()
    
    def get_valid_certificates(self, taxpayer_id: UUID) -> List[TaxCertificateModel]:
        """Get valid (not expired) certificates"""
        now = datetime.now()
        return self.db.query(TaxCertificateModel).filter(
            and_(
                TaxCertificateModel.taxpayer_id == taxpayer_id,
                TaxCertificateModel.status == 'ISSUED',
                or_(
                    TaxCertificateModel.expires_at.is_(None),
                    TaxCertificateModel.expires_at >= now
                )
            )
        ).all()
    
    def create_certificate(
        self,
        taxpayer_id: UUID,
        **cert_data
    ) -> TaxCertificateModel:
        """Create certificate for taxpayer"""
        certificate = TaxCertificateModel(
            taxpayer_id=taxpayer_id,
            **cert_data
        )
        self.db.add(certificate)
        self.db.flush()
        return certificate
    
    # ============ AGGREGATE SUMMARY ============
    
    def get_aggregate_summary(self, taxpayer_id: UUID) -> Dict[str, Any]:
        """Get complete aggregate summary for taxpayer"""
        taxpayer = self.get_by_id(taxpayer_id)
        if not taxpayer:
            return {}
        
        declarations = self.get_declarations(taxpayer_id)
        debts = self.get_debts(taxpayer_id, include_paid=False)
        payments = self.get_payments(taxpayer_id)
        certificates = self.get_certificates(taxpayer_id)
        
        total_debt = self.get_total_debt(taxpayer_id)
        total_paid = self.get_total_paid(taxpayer_id)
        overdue = self.get_overdue_debts(taxpayer_id)
        
        return {
            'taxpayer_id': str(taxpayer_id),
            'taxpayer_nif': taxpayer.nif,
            'taxpayer_name': taxpayer.name,
            'declarations_count': len(declarations),
            'pending_declarations': len([d for d in declarations if d.status == 'PENDING']),
            'debts_count': len(debts),
            'overdue_debts': len(overdue),
            'payments_count': len(payments),
            'certificates_count': len(certificates),
            'total_debt': float(total_debt),
            'total_paid': float(total_paid),
            'status': taxpayer.status,
        }
