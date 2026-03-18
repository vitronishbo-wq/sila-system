from app.core.bridges.citizen_repository_bridge import CitizenRepository as CanonicalCitizenRepository

class CitizenRepository(CanonicalCitizenRepository):
    pass

class LegacyCitizenRepository(CanonicalCitizenRepository):
    pass
__all__ = ['CitizenRepository', 'LegacyCitizenRepository']
