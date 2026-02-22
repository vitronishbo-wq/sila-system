"""
Camada de Infraestrutura - Módulo Identidade Civil

Esta camada contém implementações específicas de persistência e integrações externas.
Services e Application Layer NÃO devem conhecer detalhes de SQLAlchemy diretamente.
"""
from .repositories import (
    CitizenRepository,
    DocumentRepository,
    BIRepository,
    IdentityRequestRepository,
)

__all__ = [
    "CitizenRepository",
    "DocumentRepository",
    "BIRepository",
    "IdentityRequestRepository",
]
