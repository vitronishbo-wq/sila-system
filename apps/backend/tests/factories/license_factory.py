"""
Factory for creating License test instances.
"""
import uuid
import factory
from faker import Faker
from modules.identity.models.identity import Identity
from tests.factories.base_factory import BaseFactory

fake = Faker('pt_BR')

class LicenseFactory(BaseFactory):
    """
    Factory for creating License instances for testing (Placeholder).
    """

    class Meta:
        model = Identity
        strategy = factory.BUILD_STRATEGY

    id = factory.LazyFunction(uuid.uuid4)
    identity_type = "BI"
    identity_number = factory.Sequence(lambda n: f"LICENSE-{n}")
    user_id = 1
