"""Domain repository interfaces for Energy module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IEnergyRepository = RepositoryFactory.create_repository_interface('Energy')
__all__ = ['IEnergyRepository']