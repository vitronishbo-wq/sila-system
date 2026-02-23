from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime

from app.core.iam.domain.models.audit_log import AuditLog
from app.core.iam.domain.enums.user_status import AuditAction, ResourceType


class AuditRepositoryPort(ABC):
    """Interface do repositório de auditoria"""
    
    @abstractmethod
    def save(self, log: AuditLog) -> AuditLog:
        """Salva um log de auditoria"""
        pass
    
    @abstractmethod
    def get_by_id(self, log_id: str) -> Optional[AuditLog]:
        """Busca log por ID"""
        pass
    
    @abstractmethod
    def get_by_user(self, user_id: str, 
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   limit: int = 100) -> List[AuditLog]:
        """Busca logs por usuário"""
        pass
    
    @abstractmethod
    def get_by_resource(self, resource: ResourceType, resource_id: str,
                       limit: int = 100) -> List[AuditLog]:
        """Busca logs por recurso específico"""
        pass
    
    @abstractmethod
    def get_by_action(self, action: AuditAction,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None,
                     limit: int = 100) -> List[AuditLog]:
        """Busca logs por ação"""
        pass
    
    @abstractmethod
    def search(self, filters: Dict[str, Any],
              start_date: Optional[datetime] = None,
              end_date: Optional[datetime] = None,
              skip: int = 0, limit: int = 100) -> Tuple[List[AuditLog], int]:
        """Pesquisa avançada de logs"""
        pass
    
    @abstractmethod
    def get_user_activity_summary(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Resumo de atividade de um usuário"""
        pass
    
    @abstractmethod
    def get_resource_timeline(self, resource: ResourceType, resource_id: str) -> List[AuditLog]:
        """Linha do tempo de um recurso"""
        pass
    
    @abstractmethod
    def get_failed_logins(self, username: Optional[str] = None,
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None,
                         limit: int = 100) -> List[AuditLog]:
        """Busca tentativas de login falhas"""
        pass
