"""
Repositórios do Módulo Identidade Civil

Padrão Repository: Abstrair o acesso a dados para que Application Layer
não conheça detalhes de implementação (SQLAlchemy, Redis, etc).
"""
from .citizen_repository import CitizenRepository
from .document_repository import DocumentRepository
from .bi_repository import BIRepository
from .identity_request_repository import IdentityRequestRepository

__all__ = [
    "CitizenRepository",
    "DocumentRepository",
    "BIRepository",
    "IdentityRequestRepository",
]