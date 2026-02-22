from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from uuid import UUID


class AuditPort(ABC):
    """Interface para auditoria"""
    
    @abstractmethod
    async def log(self, action: str, user_id: Optional[UUID], entity_id: Optional[UUID],
                 entity_type: str, details: Dict[str, Any], ip_address: Optional[str] = None,
                 user_agent: Optional[str] = None):
        """Regista uma ação de auditoria"""
        pass
    
    @abstractmethod
    async def log_taxpayer_access(self, taxpayer_id: UUID, accessed_by: UUID,
                                 access_type: str, ip_address: Optional[str] = None):
        """Regista acesso a dados de contribuinte"""
        pass
    
    @abstractmethod
    async def log_tax_declaration(self, declaration_id: UUID, action: str,
                                 user_id: UUID, changes: Dict[str, Any]):
        """Regista ação em declaração fiscal"""
        pass
    
    @abstractmethod
    async def log_payment(self, payment_id: UUID, action: str,
                         user_id: UUID, amount: float, method: str):
        """Regista ação de pagamento"""
        pass
    
    @abstractmethod
    async def log_agt_sync(self, taxpayer_id: UUID, sync_type: str,
                          status: str, details: Dict[str, Any]):
        """Regista sincronização com AGT"""
        pass
    
    @abstractmethod
    async def log_error(self, error_type: str, message: str,
                       details: Dict[str, Any], user_id: Optional[UUID] = None):
        """Regista erro do sistema"""
        pass
    
    @abstractmethod
    async def get_taxpayer_history(self, taxpayer_id: UUID, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtém histórico de um contribuinte"""
        pass
    
    @abstractmethod
    async def search_audit(self, filters: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Pesquisa logs de auditoria"""
        pass
