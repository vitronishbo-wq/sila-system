"""
Factory for creating Citizen test instances.
"""
import uuid
from datetime import datetime, timezone, date
import factory
from faker import Faker
from modules.citizenship.models.citizen import Citizen
from tests.factories.base_factory import BaseFactory

fake = Faker('pt_BR')

class CitizenFactory(BaseFactory):
    """
    Factory for creating Citizen instances for testing.
    """

    class Meta:
        model = Citizen
        strategy = factory.BUILD_STRATEGY

    # Core identification
    id = factory.Sequence(lambda n: n)
    full_name = factory.LazyFunction(lambda: fake.name())
    cpf = factory.Sequence(lambda n: f"{n:011}")
    birth_date = factory.LazyFunction(lambda: fake.date_of_birth(minimum_age=16, maximum_age=100))
    gender = factory.LazyFunction(lambda: fake.random_element(elements=('M', 'F', 'O', 'N')))
    
    # Contact information
    email = factory.LazyFunction(lambda: fake.email())
    phone_number = factory.LazyFunction(lambda: fake.phone_number()[:20])

    # Address information
    address_zip_code = factory.LazyFunction(lambda: fake.postcode())
    address_street = factory.LazyFunction(lambda: fake.street_name())
    address_number = factory.LazyFunction(lambda: str(fake.building_number()))
    address_neighborhood = factory.LazyFunction(lambda: fake.bairro())
    address_city = factory.LazyFunction(lambda: fake.city())
    address_state = factory.LazyFunction(lambda: fake.estado_sigla())

    # Status and metadata
    is_active = True
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyAttribute(lambda o: o.created_at)
