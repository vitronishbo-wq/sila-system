"""
Serviço de health para o dashboard (stub minimal).
Este arquivo fornece uma implementação mínima de HealthService para evitar
erros de importação durante a inicialização. Expanda com lógica real
quando necessário.
"""

from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession


class HealthService:
    """Serviço mínimo para retornar informações de saúde do sistema."""

    def __init__(self, db: AsyncSession | None = None):
        self.db = db

    async def get_overall_health(self) -> Dict[str, Any]:
        """Retorna um dicionário com status simplificado de saúde."""
        return {
            "status": "healthy",
            "components": {
                "database": "up",
                "cache": "up",
                "api": "up",
            },
        }

    async def get_service_health(self, service_name: str) -> Dict[str, Any]:
        """Retorna estado simulado para um serviço específico."""
        return {"service": service_name, "status": "up"}
