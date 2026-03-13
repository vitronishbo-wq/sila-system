"""Domain module - DDD aggregates and entities"""
from .base_aggregate import BaseAggregate, DomainEvent
__all__ = ['BaseAggregate', 'DomainEvent']