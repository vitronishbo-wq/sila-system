"""Domain repository interfaces for Compliance module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IComplianceRepository = RepositoryFactory.create_repository_interface('Compliance')
__all__ = ['IComplianceRepository']