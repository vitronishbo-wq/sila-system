"""Domain repository interfaces for Logistics module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
ILogisticsRepository = RepositoryFactory.create_repository_interface('Logistics')
__all__ = ['ILogisticsRepository']