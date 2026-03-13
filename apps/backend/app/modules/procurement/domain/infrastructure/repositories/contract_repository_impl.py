from app.platform.persistence.base_repository import BaseRepository
from ...domain.repositories.contract_repository import ContractRepository
from ..orm.contract_model import ContractModel

class ContractRepositoryImpl(BaseRepository[ContractModel], ContractRepository):

    def __init__(self):
        super().__init__(ContractModel)

    def get(self, contract_id):
        return super().get_by_id(self._db, contract_id) if hasattr(self, '_db') else None

    def save(self, contract):
        return contract