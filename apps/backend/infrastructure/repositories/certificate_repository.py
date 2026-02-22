from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ...domain.models.certificate_record import CertificateRecord
from ...domain.enums import CertificateType, CertificateStatus
from ...domain.value_objects import CertificateNumber, RegistryOffice
from ..models.certificate_model import CertificateModel
from .base_repository import BaseRepository
from ...application.ports.certificate_repository_port import CertificateRepositoryPort


class CertificateRepository(BaseRepository[CertificateModel], CertificateRepositoryPort):
    """Implementação do repositório de certificados"""
    
    def __init__(self, db: Session):
        super().__init__(db, CertificateModel)
    
    def save(self, certificate: CertificateRecord) -> CertificateRecord:
        """Salva um certificado"""
        # Converte domain para model
        model_data = {
            "id": certificate.id,
            "certificate_number": str(certificate.certificate_number) if certificate.certificate_number else None,
            "certificate_type": certificate.certificate_type,
            "event_id": certificate.event_id,
            "event_type": certificate.event_type,
            "citizen_id": certificate.citizen_id,
            "citizen_name": certificate.citizen_name,
            "full_content": certificate.full_content,
            "summary": certificate.summary,
            "issue_date": certificate.issue_date,
            "issue_office_name": certificate.issue_office.name if certificate.issue_office else None,
            "issue_office_code": certificate.issue_office.code if certificate.issue_office else None,
            "issue_office_province": certificate.issue_office.province if certificate.issue_office else None,
            "issue_office_municipality": certificate.issue_office.municipality if certificate.issue_office else None,
            "issued_by": certificate.issued_by,
            "status": certificate.status,
            "is_authenticated": certificate.is_authenticated,
            "authentication_code": certificate.authentication_code,
            "authentication_date": certificate.authentication_date,
            "original_certificate_id": certificate.original_certificate_id,
            "is_duplicate": certificate.is_duplicate,
            "duplicate_reason": certificate.duplicate_reason,
            "pdf_path": certificate.pdf_path,
            "qr_code": certificate.qr_code,
            "metadata": certificate.metadata,
            "version": getattr(certificate, 'version', 1),
            "created_at": certificate.created_at,
            "updated_at": certificate.updated_at,
            "created_by": certificate.created_by,
        }
        
        # Verifica se já existe
        existing = super().get_by_id(certificate.id)
        if existing:
            # Atualiza
            if existing:
                for key, value in model_data.items():
                    if value is not None:
                        setattr(existing, key, value)
                existing.updated_at = datetime.now()
                self.db.flush()
                return self._to_domain(existing)
        else:
            # Cria novo
            model = CertificateModel(**model_data)
            self.db.add(model)
            self.db.flush()
            return self._to_domain(model)
        
        return certificate
    
    def get_by_id(self, certificate_id: str) -> Optional[CertificateRecord]:
        """Busca certificado por ID"""
        model = super().get_by_id(certificate_id)
        return self._to_domain(model) if model else None
    
    def get_by_number(self, certificate_number: CertificateNumber) -> Optional[CertificateRecord]:
        """Busca certificado por número"""
        model = self.db.query(CertificateModel).filter(
            CertificateModel.certificate_number == str(certificate_number),
            CertificateModel.is_active == True
        ).first()
        return self._to_domain(model) if model else None
    
    def get_by_event_id(self, event_id: str) -> List[CertificateRecord]:
        """Busca certificados por ID do evento"""
        models = self.db.query(CertificateModel).filter(
            CertificateModel.event_id == event_id,
            CertificateModel.is_active == True
        ).order_by(CertificateModel.issue_date.desc()).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_citizen_id(self, citizen_id: str,
                          cert_type: Optional[CertificateType] = None) -> List[CertificateRecord]:
        """Busca certificados por ID do cidadão"""
        query = self.db.query(CertificateModel).filter(
            CertificateModel.citizen_id == citizen_id,
            CertificateModel.is_active == True
        )
        
        if cert_type:
            cert_type_value = cert_type.value if hasattr(cert_type, 'value') else cert_type
            query = query.filter(CertificateModel.certificate_type == cert_type_value)
        
        models = query.order_by(CertificateModel.issue_date.desc()).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_status(self, status: CertificateStatus) -> List[CertificateRecord]:
        """Busca certificados por status"""
        status_value = status.value if hasattr(status, 'value') else status
        models = self.db.query(CertificateModel).filter(
            CertificateModel.status == status_value,
            CertificateModel.is_active == True
        ).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_date_range(self, start_date: date, end_date: date) -> List[CertificateRecord]:
        """Busca certificados por intervalo de datas"""
        models = self.db.query(CertificateModel).filter(
            CertificateModel.issue_date.between(start_date, end_date),
            CertificateModel.is_active == True
        ).all()
        return [self._to_domain(m) for m in models]
    
    def get_by_authentication_code(self, auth_code: str) -> Optional[CertificateRecord]:
        """Busca certificado por código de autenticação"""
        model = self.db.query(CertificateModel).filter(
            CertificateModel.authentication_code == auth_code,
            CertificateModel.is_active == True
        ).first()
        return self._to_domain(model) if model else None
    
    def update_status(self, certificate_id: str, status: CertificateStatus,
                     user_id: str, reason: Optional[str] = None) -> Optional[CertificateRecord]:
        """Atualiza status do certificado"""
        model = super().get_by_id(certificate_id)
        if not model:
            return None
        
        status_value = status.value if hasattr(status, 'value') else status
        model.status = status_value
        model.updated_by = user_id
        model.updated_at = datetime.now()
        
        if reason:
            if not model.metadata:
                model.metadata = {}
            model.metadata["status_change_reason"] = reason
            model.metadata["status_changed_at"] = datetime.now().isoformat()
            model.metadata["status_changed_by"] = user_id
        
        self.db.flush()
        return self._to_domain(model)
    
    def get_next_sequence_number(self, year: int, cert_type: str) -> int:
        """Obtém próximo número sequencial para certificado"""
        type_prefix = {
            "CERTIDAO_NASCIMENTO": "NASC",
            "CERTIDAO_CASAMENTO": "CASA",
            "CERTIDAO_OBITO": "OBITO"
        }.get(cert_type, "CERT")
        
        pattern = f"CERT/{year}/{type_prefix}/%"
        
        count = self.db.query(CertificateModel).filter(
            CertificateModel.certificate_number.like(pattern)
        ).count()
        
        return count + 1
    
    def find_duplicates(self, event_id: str) -> List[CertificateRecord]:
        """Busca certificados duplicados (segundas vias) de um evento"""
        models = self.db.query(CertificateModel).filter(
            CertificateModel.event_id == event_id,
            CertificateModel.is_duplicate == True,
            CertificateModel.is_active == True
        ).all()
        return [self._to_domain(m) for m in models]
    
    def get_latest_by_event(self, event_id: str) -> Optional[CertificateRecord]:
        """Obtém o certificado mais recente de um evento"""
        model = self.db.query(CertificateModel).filter(
            CertificateModel.event_id == event_id,
            CertificateModel.is_active == True
        ).order_by(CertificateModel.issue_date.desc()).first()
        return self._to_domain(model) if model else None
    
    def delete(self, certificate_id: str, soft_delete: bool = True) -> bool:
        """Remove certificado"""
        return super().delete(certificate_id, soft_delete)
    
    def _to_domain(self, model: CertificateModel) -> Optional[CertificateRecord]:
        """Converte model para domain object"""
        if not model:
            return None
        
        certificate = CertificateRecord(
            id=model.id,
            certificate_number=CertificateNumber(model.certificate_number) if model.certificate_number else None,
            certificate_type=model.certificate_type,
            event_id=model.event_id,
            event_type=model.event_type,
            citizen_id=model.citizen_id,
            citizen_name=model.citizen_name,
            full_content=model.full_content,
            summary=model.summary,
            issue_date=model.issue_date,
            issue_office=RegistryOffice(
                name=model.issue_office_name,
                code=model.issue_office_code,
                province=model.issue_office_province,
                municipality=model.issue_office_municipality
            ) if model.issue_office_code else None,
            issued_by=model.issued_by,
            status=model.status,
            is_authenticated=model.is_authenticated,
            authentication_code=model.authentication_code,
            authentication_date=model.authentication_date,
            original_certificate_id=model.original_certificate_id,
            is_duplicate=model.is_duplicate,
            duplicate_reason=model.duplicate_reason,
            pdf_path=model.pdf_path,
            qr_code=model.qr_code,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
            metadata=model.metadata
        )
        
        # Adiciona versão como atributo extra
        certificate.version = model.version
        
        return certificate
