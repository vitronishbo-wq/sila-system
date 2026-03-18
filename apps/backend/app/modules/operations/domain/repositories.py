"""Domain repository interfaces for Operations module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IOperationsRepository = RepositoryFactory.create_repository_interface('Operations')
__all__ = ['IOperationsRepository']