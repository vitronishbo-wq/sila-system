from uuid import UUID
from typing import Dict, Any


class NotificationClient:
    """Cliente para notificações"""
    
    def notify_citizen(self, citizen_id: UUID, title: str, message: str,
                       data: Dict[str, Any] = None):
        """Notifica um cidadão"""
        # Em produção, integraria com SMS/Email/Push
        print(f"[NOTIFICATION] Citizen {citizen_id}: {title} - {message}")
    
    def notify_operator(self, user_id: UUID, title: str, message: str,
                        data: Dict[str, Any] = None):
        """Notifica um operador"""
        print(f"[NOTIFICATION] Operator {user_id}: {title} - {message}")
    
    def notify_managers(self, title: str, message: str,
                        data: Dict[str, Any] = None):
        """Notifica gestores"""
        print(f"[NOTIFICATION] Managers: {title} - {message}")
