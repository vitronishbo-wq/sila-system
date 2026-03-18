"""Domain repository interfaces for PublicSecurity module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
IPublicSecurityRepository = RepositoryFactory.create_repository_interface('PublicSecurity')
__all__ = ['IPublicSecurityRepository']