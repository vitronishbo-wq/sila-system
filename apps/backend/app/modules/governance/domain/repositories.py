"""Domain repository interfaces for Governance module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IGovernanceRepository = RepositoryFactory.create_repository_interface('Governance')
__all__ = ['IGovernanceRepository']