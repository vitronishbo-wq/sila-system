"""
Factory for creating User test instances.

This module provides a UserFactory for generating test User instances with realistic fake data.
"""

import uuid
from datetime import UTC, datetime

import factory
from faker import Faker
from tests.factories.base_factory import BaseFactory

from apps.backend.app.modules.identity.models.user import AdministrativeLevel, User

fake = Faker()


class UserFactory(BaseFactory):
    """
    Factory for creating User instances for testing.
    """

    class Meta:
        model = User
        strategy = factory.BUILD_STRATEGY

    # Core fields
    # id is assigned by DB if int, but let's allow it to be buildable if needed
    # The model uses id: Mapped[int] = mapped_column(primary_key=True, index=True)

    uuid = factory.LazyFunction(lambda: str(uuid.uuid4()))
    email = factory.Sequence(lambda n: f"testuser{n}_{fake.uuid4()[:8]}@sila.gov.ao")
    name = factory.LazyFunction(lambda: fake.name())
    phone = factory.LazyFunction(lambda: fake.phone_number()[:20])
    bi_number = factory.Sequence(lambda n: f"{n:09}LA{n:03}")

    # Authentication (hashed 'password')
    hashed_password = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"

    # Status flags
    is_active = True
    is_verified = True
    status = "active"

    # Administrative Level
    level = AdministrativeLevel.LOCAL
    region_id = None

    # Role-based access control
    roles = ["user"]

    # Timestamps
    created_at = factory.LazyFunction(lambda: datetime.now(UTC))
    updated_at = factory.LazyAttribute(lambda o: o.created_at)

    @classmethod
    def create_batch(cls, size, **kwargs):
        return [cls.create(**kwargs) for _ in range(size)]
