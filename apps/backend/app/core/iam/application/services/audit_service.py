from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session as SQLSession
from datetime import datetime, timedelta

from .base_service import BaseService, NotFoundError


class AuditService(BaseService):
    """Serviço de auditoria"""
    
    def __init__(self, db: SQLSession):
        super().__init__(db)
    
    def log(self, log_data: Dict[str, Any]):
        """
        Registra um log de auditoria
        """
        from ...infrastructure.models.audit_model import AuditLogModel
        
        log = AuditLogModel(
            action=log_data.get("action"),
            resource_type=log_data.get("resource"),
            user_id=log_data.get("user_id"),
            resource_id=log_data.get("resource_id"),
            details=log_data.get("details", {}),
            success=log_data.get("success", True),
            error_message=log_data.get("error_message")
        )
        
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        
        return log
    
    def get_log(self, log_id: str):
        """
        Busca log por ID
        """
        log = self.audit_repo.get_by_id(log_id)
        if not log:
            raise NotFoundError("AuditLog", log_id)
        return log
    
    def list_logs(self, skip: int = 0, limit: int = 100, 
                  filters: Optional[Dict[str, Any]] = None) -> Tuple[List, int]:
        """
        Lista logs com filtros
        """
        return self.audit_repo.search(filters or {}, skip=skip, limit=limit)
    
    def get_user_logs(self, user_id: str, days: int = 30, limit: int = 100) -> List:
        """
        Busca logs de um usuário
        """
        start_date = datetime.now() - timedelta(days=days)
        return self.audit_repo.get_by_user(user_id, start_date=start_date, limit=limit)
    
    def get_resource_history(self, resource: str, resource_id: str, 
                            limit: int = 100) -> List:
        """
        Busca histórico de um recurso
        """
        return self.audit_repo.get_resource_timeline(resource, resource_id)[:limit]
    
    def get_failed_logins(self, username: Optional[str] = None, 
                          days: int = 7, limit: int = 100) -> List:
        """
        Busca tentativas de login falhas
        """
        start_date = datetime.now() - timedelta(days=days)
        return self.audit_repo.get_failed_logins(
            username=username,
            start_date=start_date,
            limit=limit
        )
    
    def get_user_summary(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Resumo de atividades de um usuário
        """
        return self.audit_repo.get_user_activity_summary(user_id, days)
    
    def export_logs(self, start_date: datetime, end_date: datetime, 
                   format: str = "json") -> List[Dict[str, Any]]:
        """
        Exporta logs para análise
        """
        logs, _ = self.audit_repo.search(
            filters={},
            skip=0,
            limit=10000
        )
        
        return [log.to_dict() if hasattr(log, 'to_dict') else log.__dict__ for log in logs]
