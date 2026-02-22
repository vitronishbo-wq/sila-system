"""
Factory for creating Service test instances.
"""
import uuid
from datetime import datetime, timezone
import factory
from faker import Faker
from modules.citizenship.models.citizenship_models import CitizenshipService
from tests.factories.base_factory import BaseFactory

fake = Faker('pt_BR')

class ServiceFactory(BaseFactory):
    """
    Factory for creating Service instances for testing.
    """

    class Meta:
        model = CitizenshipService
        strategy = factory.BUILD_STRATEGY

    id = factory.Sequence(lambda n: n)
    name = factory.LazyFunction(lambda: f"Serviço de {fake.catch_phrase()}")
    description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=3))
    is_active = True
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyAttribute(lambda o: o.created_at)
