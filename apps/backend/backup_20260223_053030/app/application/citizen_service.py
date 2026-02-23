from typing import List, Optional
from uuid import UUID
from .ports.citizen_repository_port import CitizenRepositoryPort
from ..domain.citizen import Citizen

class CitizenService:
    def __init__(self, repository: CitizenRepositoryPort):
        self.repository = repository

    async def create_citizen(self, citizen: Citizen) -> Citizen:
        return await self.repository.add(citizen)

    async def update_citizen(self, citizen: Citizen) -> Citizen:
        return await self.repository.update(citizen)

    async def get_citizen_by_id(self, id: UUID) -> Optional[Citizen]:
        return await self.repository.get_by_id(id)

    async def get_citizen_by_national_id_number(self, national_id_number: str) -> Optional[Citizen]:
        return await self.repository.get_by_national_id_number(national_id_number)

    async def get_citizen_by_nif(self, nif: str) -> Optional[Citizen]:
        return await self.repository.get_by_nif(nif)

    async def list_citizens(self, filters: dict, limit: int, offset: int) -> List[Citizen]:
        return await self.repository.list(filters=filters, limit=limit, offset=offset)

    async def soft_delete_citizen(self, id: UUID) -> None:
        await self.repository.soft_delete(id)
