"""Domain repository interfaces for Resources module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IResourcesRepository = RepositoryFactory.create_repository_interface('Resources')
__all__ = ['IResourcesRepository']