"""Domain repository interfaces for Procurement module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IProcurementRepository = RepositoryFactory.create_repository_interface('Procurement')
__all__ = ['IProcurementRepository']