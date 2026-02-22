"""
Módulo de Notificações do SILA.

Este módulo fornece funcionalidades completas para:
- Gestão multicanal de notificações (email, SMS, push, in-app)
- Templates reutilizáveis de mensagens
- Controle de fila e agendamento automático
- Eventos automáticos baseados em triggers do sistema
- Webhooks para integração com sistemas externos
- Configurações personalizadas por usuário
- Relatórios e métricas de entrega detalhados
- Auditoria completa de todas as operações
"""

"""Module initialization with path configuration."""

import sys
from pathlib import Path

# Ensure backend is in path for imports
_backend_path = Path(__file__).parent.parent.parent
if str(_backend_path) not in sys.path:
    sys.path.insert(0, str(_backend_path))

from typing import Any, Dict, List, Optional, Type, Union

from fastapi import FastAPI, HTTPException, Request, status

# Core exports
__all__ = [
    # Exception classes
    "NotificationError",
    "NotificationNotFoundError",
    "NotificationDeliveryError",
    "NotificationTemplateError",
    "NotificationQueueError",
    # Handler functions
    "notification_exception_handler",
    "register_exception_handlers",
    "setup_error_handling",
    "setup_notifications_module",
    "ERROR_RESPONSES",
    # Modules
    "crud",
    "schemas",
    "models",
    "services",
    "endpoints",
    # Service classes
    "NotificationService",
]

# Avoid importing subpackages at module import time to prevent circular imports.
# Consumers should import specific submodules, e.g. `from modules.notifications import endpoints as notifications`.


def setup_notifications_module(app: FastAPI) -> None:
    """
    Configura o módulo de notificações na aplicação FastAPI.

    Args:
        app: Instância da aplicação FastAPI
    """
    # Configure error handling (se existir)
    # setup_error_handling(app)

    # Import router here to avoid circular imports
    from .endpoints import router as notifications_router

    # Include the router
    app.include_router(
        notifications_router, prefix="/api/v1/notifications", tags=["notifications"]
    )

    # Log setup completion
    import logging

    logger = logging.getLogger(__name__)
    logger.info("Módulo de Notificações configurado com sucesso")
