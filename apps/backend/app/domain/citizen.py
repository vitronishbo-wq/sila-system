from uuid import UUID
from datetime import date
from .enums import GenderEnum, MaritalStatusEnum, CitizenStatusEnum
from .value_objects import NationalId, NIF

class Citizen:
    def __init__(
        self,
        id: UUID,
        national_id_number: NationalId,
        nif: NIF,
        first_name: str,
        last_name: str,
        full_name: str,
        gender: GenderEnum,
        birth_date: date,
        marital_status: MaritalStatusEnum,
        nationality: str,
        place_of_birth: str,
        father_name: str,
        mother_name: str,
        phone: str,
        email: str,
        province: str,
        municipality: str,
        commune: str,
        neighborhood: str,
        street: str,
        house_number: str,
        status: CitizenStatusEnum,
        is_verified: bool,
        verification_level: str,
        created_at: date,
        updated_at: date,
        created_by: str,
        updated_by: str,
        # Foreign keys futuras
        user_id: UUID = None,
        household_id: UUID = None,
        taxpayer_profile_id: UUID = None,
        employment_profile_id: UUID = None,
        health_profile_id: UUID = None,
        education_profile_id: UUID = None,
    ):
        self.id = id
        self.national_id_number = national_id_number
        self.nif = nif
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.gender = gender
        self.birth_date = birth_date
        self.marital_status = marital_status
        self.nationality = nationality
        self.place_of_birth = place_of_birth
        self.father_name = father_name
        self.mother_name = mother_name
        self.phone = phone
        self.email = email
        self.province = province
        self.municipality = municipality
        self.commune = commune
        self.neighborhood = neighborhood
        self.street = street
        self.house_number = house_number
        self.status = status
        self.is_verified = is_verified
        self.verification_level = verification_level
        self.created_at = created_at
        self.updated_at = updated_at
        self.created_by = created_by
        self.updated_by = updated_by
        self.user_id = user_id
        self.household_id = household_id
        self.taxpayer_profile_id = taxpayer_profile_id
        self.employment_profile_id = employment_profile_id
        self.health_profile_id = health_profile_id
        self.education_profile_id = education_profile_id
