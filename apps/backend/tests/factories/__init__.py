"""
Factories para geração de dados de teste
"""

import factory
from datetime import date
from uuid import uuid4

from apps.backend.app.core.bridges.identity_bridge import CitizenFUC

Citizen = CitizenFUC
CitizenModel = CitizenFUC


class CitizenFactory(factory.Factory):
    """Factory para entidades Citizen de domínio"""
    
    class Meta:
        model = Citizen
    
    citizen_id = factory.LazyFunction(uuid4)
    full_name = factory.Faker("name")
    document_number = factory.Faker("bothify", text="????????-????")
    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=80)
    gender = factory.Faker("random_element", elements=["M", "F", "O"])
    phone = factory.Faker("phone_number")
    email = factory.Faker("email")
    vital_status = "alive"


class CitizenModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory para modelos SQLAlchemy CitizenModel"""
    
    class Meta:
        model = CitizenModel
        sqlalchemy_session_persistence = "flush"
        # Session will be provided at instantiation via sqlalchemy_session parameter
    
    citizen_id = factory.LazyFunction(uuid4)
    full_name = factory.Faker("name")
    document_number = factory.Faker("bothify", text="????????-????")
    birth_date = factory.Faker("date_of_birth", minimum_age=18, maximum_age=80)
    gender = factory.Faker("random_element", elements=["M", "F"])
    phone = factory.Faker("phone_number")
    email = factory.Faker("email")
    vital_status = "alive"


class InactiveCitizenFactory(factory.Factory):
    """Factory para cidadãos inativos"""
    
    class Meta:
        model = Citizen
    
    citizen_id = factory.LazyFunction(uuid4)
    full_name = factory.Faker("name")
    birth_date = factory.Faker("date_between", start_date="-100y", end_date="-20y")
    vital_status = "deceased"
