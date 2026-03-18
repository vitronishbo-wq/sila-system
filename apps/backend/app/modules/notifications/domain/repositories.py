"""Domain repository interfaces for Notifications module"""
from abc import ABC
from typing import Generic, TypeVar
from apps.backend.core.repositories.repository_factory import RepositoryFactory
T = TypeVar('T')
INotificationsRepository = RepositoryFactory.create_repository_interface('Notifications')
__all__ = ['INotificationsRepository']