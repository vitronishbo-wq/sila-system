"""Domain repository interfaces for MigrationService module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IMigrationServiceRepository = RepositoryFactory.create_repository_interface('MigrationService')
__all__ = ['IMigrationServiceRepository']