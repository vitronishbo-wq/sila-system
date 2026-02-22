from typing import Optional, TypeVar, Generic
from sqlalchemy.orm import Session
import logging

from ...infrastructure.repositories.unit_of_work import UnitOfWorkFactory
from ...infrastructure.repositories.citizen_repository import CitizenRepository
from ...infrastructure.repositories.civil_event_repository import CivilEventRepository
from ...infrastructure.repositories.certificate_repository import CertificateRepository
from ...utils.audit import AuditService

T = TypeVar('T')


class BaseService(Generic[T]):
    """Classe base para todos os serviços"""
    
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Repositórios
        self.citizen_repo = CitizenRepository(db)
        self.event_repo = CivilEventRepository(db)
        self.certificate_repo = CertificateRepository(db)
        
        # Serviços auxiliares
        self.audit = AuditService(db)
        self.uow_factory = UnitOfWorkFactory()
    
    def _log_action(self, action: str, entity_id: str, entity_type: str, 
                   user_id: str, changes: Optional[dict] = None):
        """Regista ação para auditoria"""
        self.audit.log_event(
            event_type="SERVICE",
            entity_id=entity_id,
            entity_type=entity_type,
            action=action,
            user_id=user_id,
            changes=changes
        )
    
    def _handle_error(self, error: Exception, context: dict = None):
        """Trata erros de forma consistente"""
        self.logger.error(f"Erro: {str(error)}", exc_info=True, extra=context or {})
        raise error
