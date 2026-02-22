from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import date


class NotificationPort(ABC):
    """Interface para envio de notificações"""
    
    @abstractmethod
    async def notify_taxpayer(self, taxpayer_id: UUID, title: str, message: str,
                              data: Optional[Dict[str, Any]] = None, channel: str = "all"):
        """Notifica um contribuinte"""
        pass
    
    @abstractmethod
    async def notify_admin(self, title: str, message: str,
                          data: Optional[Dict[str, Any]] = None):
        """Notifica administradores do sistema"""
        pass
    
    @abstractmethod
    async def notify_operator(self, user_id: UUID, title: str, message: str,
                             data: Optional[Dict[str, Any]] = None):
        """Notifica um operador específico"""
        pass
    
    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str,
                        html: Optional[str] = None, attachments: Optional[List[str]] = None):
        """Envia email"""
        pass
    
    @abstractmethod
    async def send_sms(self, to: str, message: str):
        """Envia SMS"""
        pass
    
    @abstractmethod
    async def send_push(self, user_id: UUID, title: str, body: str,
                       data: Optional[Dict[str, Any]] = None):
        """Envia notificação push"""
        pass
    
    @abstractmethod
    async def notify_debt_created(self, taxpayer_id: UUID, debt_amount: float, due_date: date):
        """Notifica sobre criação de dívida"""
        pass
    
    @abstractmethod
    async def notify_debt_overdue(self, taxpayer_id: UUID, debt_amount: float, days_overdue: int):
        """Notifica sobre dívida vencida"""
        pass
    
    @abstractmethod
    async def notify_declaration_approved(self, taxpayer_id: UUID, declaration_number: str):
        """Notifica sobre declaração aprovada"""
        pass
    
    @abstractmethod
    async def notify_payment_received(self, taxpayer_id: UUID, amount: float, payment_number: str):
        """Notifica sobre pagamento recebido"""
        pass
    
    @abstractmethod
    async def notify_certificate_issued(self, taxpayer_id: UUID, certificate_type: str, certificate_number: str):
        """Notifica sobre certidão emitida"""
        pass
