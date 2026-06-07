from apps.backend.app.platform.persistence.base_repository import BaseRepository

from ...domain.repositories.supplier_repository import SupplierRepository
from ..orm.supplier_model import SupplierModel


class SupplierRepositoryImpl(BaseRepository[SupplierModel], SupplierRepository):
    def __init__(self):
        super().__init__(SupplierModel)

    def get(self, supplier_id):
        return super().get_by_id(self._db, supplier_id) if hasattr(self, "_db") else None

    def save(self, supplier):
        return supplier
