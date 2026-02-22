from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc
from datetime import datetime, timedelta

from ..models.audit_model import AuditLogModel
from .base_repository import BaseRepository


class AuditRepository(BaseRepository[AuditLogModel]):
    """Implementação do repositório de auditoria"""
    
    def __init__(self, db: Session):
        super().__init__(db, AuditLogModel)
    
    def save(self, log_data: dict) -> AuditLogModel:
        """Salva um log de auditoria"""
        model = AuditLogModel(**log_data)
        self.db.add(model)
        self.db.flush()
        return model
    
    def get_by_id(self, log_id: str) -> Optional[AuditLogModel]:
        """Busca log por ID"""
        return super().get_by_id(log_id)
    
    def get_by_user(self, user_id: str, 
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   limit: int = 100) -> List[AuditLogModel]:
        """Busca logs por usuário"""
        query = self.db.query(AuditLogModel).filter(
            AuditLogModel.user_id == user_id
        )
        
        if start_date:
            query = query.filter(AuditLogModel.created_at >= start_date)
        if end_date:
            query = query.filter(AuditLogModel.created_at <= end_date)
        
        return query.order_by(desc(AuditLogModel.created_at)).limit(limit).all()
    
    def get_by_resource(self, resource: str, resource_id: str,
                       limit: int = 100) -> List[AuditLogModel]:
        """Busca logs por recurso específico"""
        return self.db.query(AuditLogModel).filter(
            AuditLogModel.resource == resource,
            AuditLogModel.resource_id == resource_id
        ).order_by(
            desc(AuditLogModel.created_at)
        ).limit(limit).all()
    
    def get_by_action(self, action: str,
                     start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None,
                     limit: int = 100) -> List[AuditLogModel]:
        """Busca logs por ação"""
        query = self.db.query(AuditLogModel).filter(
            AuditLogModel.action == action
        )
        
        if start_date:
            query = query.filter(AuditLogModel.created_at >= start_date)
        if end_date:
            query = query.filter(AuditLogModel.created_at <= end_date)
        
        return query.order_by(desc(AuditLogModel.created_at)).limit(limit).all()
    
    def search(self, filters: Dict[str, Any],
              start_date: Optional[datetime] = None,
              end_date: Optional[datetime] = None,
              skip: int = 0, limit: int = 100) -> Tuple[List[AuditLogModel], int]:
        """Pesquisa avançada de logs"""
        query = self.db.query(AuditLogModel)
        
        # Aplica filtros
        if filters.get('user_id'):
            query = query.filter(AuditLogModel.user_id == filters['user_id'])
        if filters.get('username'):
            query = query.filter(AuditLogModel.username.ilike(f"%{filters['username']}%"))
        if filters.get('action'):
            query = query.filter(AuditLogModel.action == filters['action'])
        if filters.get('resource'):
            query = query.filter(AuditLogModel.resource == filters['resource'])
        if filters.get('resource_id'):
            query = query.filter(AuditLogModel.resource_id == filters['resource_id'])
        if filters.get('success') is not None:
            query = query.filter(AuditLogModel.success == filters['success'])
        if filters.get('ip_address'):
            query = query.filter(AuditLogModel.ip_address == filters['ip_address'])
        
        # Filtros de data
        if start_date:
            query = query.filter(AuditLogModel.created_at >= start_date)
        if end_date:
            query = query.filter(AuditLogModel.created_at <= end_date)
        
        total = query.count()
        models = query.order_by(desc(AuditLogModel.created_at)).offset(skip).limit(limit).all()
        
        return models, total
    
    def get_user_activity_summary(self, user_id: str, days: int = 30) -> Dict[str, Any]:
        """Resumo de atividade de um usuário"""
        since = datetime.utcnow() - timedelta(days=days)
        
        # Total de ações
        total = self.db.query(AuditLogModel).filter(
            AuditLogModel.user_id == user_id,
            AuditLogModel.created_at >= since
        ).count()
        
        # Ações por tipo
        by_action = self.db.query(
            AuditLogModel.action,
            func.count().label('count')
        ).filter(
            AuditLogModel.user_id == user_id,
            AuditLogModel.created_at >= since
        ).group_by(AuditLogModel.action).all()
        
        # Ações por recurso
        by_resource = self.db.query(
            AuditLogModel.resource,
            func.count().label('count')
        ).filter(
            AuditLogModel.user_id == user_id,
            AuditLogModel.created_at >= since
        ).group_by(AuditLogModel.resource).all()
        
        # Taxa de sucesso
        successful = self.db.query(AuditLogModel).filter(
            AuditLogModel.user_id == user_id,
            AuditLogModel.created_at >= since,
            AuditLogModel.success == True
        ).count()
        
        success_rate = (successful / total * 100) if total > 0 else 0
        
        return {
            "user_id": user_id,
            "period_days": days,
            "total_actions": total,
            "success_rate": round(success_rate, 2),
            "by_action": {a: c for a, c in by_action},
            "by_resource": {r: c for r, c in by_resource},
            "last_activity": self.get_last_activity(user_id)
        }
    
    def get_resource_timeline(self, resource: str, resource_id: str) -> List[AuditLogModel]:
        """Linha do tempo de um recurso"""
        return self.get_by_resource(resource, resource_id, limit=100)
    
    def get_failed_logins(self, username: Optional[str] = None,
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None,
                         limit: int = 100) -> List[AuditLogModel]:
        """Busca tentativas de login falhas"""
        query = self.db.query(AuditLogModel).filter(
            AuditLogModel.action == "LOGIN_FAILED",
            AuditLogModel.success == False
        )
        
        if username:
            query = query.filter(AuditLogModel.username == username)
        if start_date:
            query = query.filter(AuditLogModel.created_at >= start_date)
        if end_date:
            query = query.filter(AuditLogModel.created_at <= end_date)
        
        return query.order_by(desc(AuditLogModel.created_at)).limit(limit).all()
    
    def get_last_activity(self, user_id: str) -> Optional[datetime]:
        """Obtém timestamp da última atividade do usuário"""
        model = self.db.query(AuditLogModel).filter(
            AuditLogModel.user_id == user_id
        ).order_by(
            desc(AuditLogModel.created_at)
        ).first()
        
        return model.created_at if model else None
