from apps.backend.app.platform.persistence.base_repository import BaseRepository

from ...domain.repositories.tender_repository import TenderRepository
from ..orm.tender_model import TenderModel


class TenderRepositoryImpl(BaseRepository[TenderModel], TenderRepository):
    def __init__(self):
        super().__init__(TenderModel)

    def get(self, tender_id):
        return super().get_by_id(self._db, tender_id) if hasattr(self, "_db") else None

    def save(self, tender):
        return tender
