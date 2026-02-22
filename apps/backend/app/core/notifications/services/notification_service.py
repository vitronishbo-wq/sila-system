import uuid
import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.notifications.models.notification import Notification, NotificationType

logger = logging.getLogger(__name__)

class NotificationService:
    """
    Serviço Transversal de Notificações do SILA.
    Gerencia alertas para cidadãos e funcionários.
    """

    def __init__(self, db: AsyncSession, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db

    async def notify_user(
        self,
        user_id: uuid.UUID,
        title: str,
        message: str,
        n_type: NotificationType = NotificationType.INFO,
        channels: list = ["db", "email"]
    ) -> Notification:
        """Cria e persiste uma notificação no banco de dados e envia para canais externos."""
        notification = None
        
        if "db" in channels:
            notification = Notification(
                id=uuid.uuid4(),
                user_id=user_id,
                title=title,
                message=message,
                notification_type=n_type.value
            )
            self.db.add(notification)
            await self.db.flush()
        
        # Simulação de envio externo
        external_channels = [c for c in channels if c != "db"]
        if external_channels:
            await self._send_external(user_id, title, message, external_channels)
            
        return notification

    async def _send_external(self, user_id: uuid.UUID, title: str, message: str, channels: list):
        """Simula o envio por SMS, Email ou Push Notification."""
        for channel in channels:
            # Em um cenário real, aqui chamaríamos SendGrid, Twilio, Firebase, etc.
            logger.info(f"📣 [EXTERNAL-{channel.upper()}] para {user_id}: {title} | {message}")

    async def notify_request_created(
        self,
        user_id: uuid.UUID,
        request_id: uuid.UUID,
        request_data: Dict[str, Any]
    ):
        """Notifica o cidadão que o seu pedido foi recebido com sucesso."""
        title = "Pedido Recebido"
        message = f"O seu pedido {str(request_id)[:8]} foi registado com sucesso e está em processamento."
        
        await self.notify_user(
            user_id=user_id,
            title=title,
            message=message,
            n_type=NotificationType.SUCCESS,
            channels=["db", "email", "push"]
        )

    async def notify_request_status_changed(
        self,
        user_id: uuid.UUID,
        request_id: uuid.UUID,
        old_status: str,
        new_status: str
    ):
        """Notifica o cidadão sobre a alteração de estado do seu pedido."""
        title = "Atualização de Estado"
        message = f"O seu pedido {str(request_id)[:8]} mudou de {old_status} para {new_status.upper()}."
        
        await self.notify_user(
            user_id=user_id,
            title=title,
            message=message,
            n_type=NotificationType.INFO,
            channels=["db", "email", "sms"] # SMS para notificações críticas de estado
        )

    async def notify_operator(
        self,
        user_id: uuid.UUID,
        title: str,
        message: str,
        data: Dict[str, Any] = None
    ):
        """Notifica um operador/funcionário sobre uma nova atribuição."""
        await self.notify_user(
            user_id=user_id,
            title=title,
            message=message,
            n_type=NotificationType.INFO,
            channels=["db", "push"] # Operadores costumam usar Push no dashboard
        )

    async def notify_request_update(
        self,
        user_id: uuid.UUID,
        request_id: uuid.UUID,
        new_status: str
    ):
        """Manteúdo para retrocompatibilidade."""
        await self.notify_request_status_changed(user_id, request_id, "...", new_status)
