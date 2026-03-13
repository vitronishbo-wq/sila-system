from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.resources.pecuaria.application.ports import AnimalRepositoryPort, PropriedadePecuariaRepositoryPort, RebanhoRepositoryPort
from app.modules.resources.pecuaria.domain.enums import Sexo, StatusAnimal, TipoAnimal
from app.modules.resources.pecuaria.domain.models.animal import Animal

class AnimalService:

    def __init__(self, animal_repo: AnimalRepositoryPort, propriedade_repo: PropriedadePecuariaRepositoryPort, rebanho_repo: RebanhoRepositoryPort):
        self.animal_repo = animal_repo
        self.propriedade_repo = propriedade_repo
        self.rebanho_repo = rebanho_repo

    async def cadastrar_animal(self, *, tipo: TipoAnimal, raca_id: UUID, sexo: Sexo, data_nascimento: date, proprietario_id: UUID, propriedade_id: UUID, brinco: str | None=None, rebanho_id: UUID | None=None) -> Animal:
        propriedade = await self.propriedade_repo.get_by_id(propriedade_id)
        if not propriedade:
            raise ValueError('Propriedade nao encontrada')
        if rebanho_id:
            rebanho = await self.rebanho_repo.get_by_id(rebanho_id)
            if not rebanho:
                raise ValueError('Rebanho nao encontrado')
        brinco_final = brinco or await self.animal_repo.next_brinco(propriedade_id)
        if await self.animal_repo.get_by_brinco(brinco_final):
            raise ValueError('Brinco ja cadastrado')
        animal = Animal.cadastrar(brinco=brinco_final, tipo=tipo, raca_id=raca_id, sexo=sexo, data_nascimento=data_nascimento, proprietario_id=proprietario_id, propriedade_id=propriedade_id, rebanho_id=rebanho_id)
        return await self.animal_repo.save(animal)

    async def buscar_animal(self, animal_id: UUID) -> Animal:
        item = await self.animal_repo.get_by_id(animal_id)
        if not item:
            raise ValueError('Animal nao encontrado')
        return item

    async def listar_animais(self, *, propriedade_id: UUID | None=None, tipo: TipoAnimal | None=None, status: StatusAnimal | None=None) -> list[Animal]:
        if propriedade_id:
            return await self.animal_repo.list_by_propriedade(propriedade_id)
        return await self.animal_repo.list_by_filtros(tipo=tipo, status=status)