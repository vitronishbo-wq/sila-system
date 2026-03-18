"""Domain repository interfaces for Society module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
ISocietyRepository = RepositoryFactory.create_repository_interface('Society')
__all__ = ['ISocietyRepository']