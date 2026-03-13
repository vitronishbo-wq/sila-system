from apps.backend.app.core.bridges.citizen_repository_bridge import CitizenRepository as CanonicalCitizenRepository

class CitizenRepository(CanonicalCitizenRepository):
    pass
__all__ = ['CitizenRepository']