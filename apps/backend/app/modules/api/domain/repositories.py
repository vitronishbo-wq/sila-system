"""Domain repository interfaces for Api module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IApiRepository = RepositoryFactory.create_repository_interface('Api')
__all__ = ['IApiRepository']