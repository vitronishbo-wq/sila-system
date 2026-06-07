"""Domain repository interfaces for Educacao module"""

from typing import TypeVar

from apps.backend.core.repositories.repository_factory import RepositoryFactory

T = TypeVar("T")
IEducacaoRepository = RepositoryFactory.create_repository_interface("Educacao")
__all__ = ["IEducacaoRepository"]
