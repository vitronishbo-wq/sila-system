"""Domain repository interfaces for Industry module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IIndustryRepository = RepositoryFactory.create_repository_interface('Industry')
__all__ = ['IIndustryRepository']