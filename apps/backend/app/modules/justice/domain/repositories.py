"""Domain repository interfaces for Justice module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IJusticeRepository = RepositoryFactory.create_repository_interface('Justice')
__all__ = ['IJusticeRepository']