from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.resources.pecuaria.application.ports import AnimalRepositoryPort
from apps.backend.app.modules.resources.pecuaria.domain.enums import Sexo, StatusAnimal, TipoAnimal
from apps.backend.app.modules.resources.pecuaria.domain.models.animal import Animal
from apps.backend.app.modules.resources.pecuaria.infrastructure.models.animal_model import AnimalModel

class SQLAlchemyAnimalRepository(AnimalRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, animal: Animal) -> Animal:
        model = await self.session.get(AnimalModel, animal.id)
        if not model:
            model = AnimalModel(id=animal.id)
            self.session.add(model)
        model.brinco = animal.brinco
        model.nome = animal.nome
        model.tipo = animal.tipo.value
        model.raca_id = animal.raca_id
        model.sexo = animal.sexo.value
        model.data_nascimento = animal.data_nascimento
        model.peso_nascimento = animal.peso_nascimento
        model.peso_atual = animal.peso_atual
        model.status = animal.status.value
        model.proprietario_id = animal.proprietario_id
        model.propriedade_id = animal.propriedade_id
        model.rebanho_id = animal.rebanho_id
        model.mae_id = animal.mae_id
        model.pai_id = animal.pai_id
        model.data_entrada = animal.data_entrada
        model.data_saida = animal.data_saida
        model.observacoes = animal.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, animal_id: UUID) -> Animal | None:
        model = await self.session.get(AnimalModel, animal_id)
        return self._to_domain(model) if model else None

    async def get_by_brinco(self, brinco: str) -> Animal | None:
        stmt = select(AnimalModel).where(AnimalModel.brinco == brinco)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_propriedade(self, propriedade_id: UUID) -> list[Animal]:
        stmt = select(AnimalModel).where(AnimalModel.propriedade_id == propriedade_id)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(model) for model in rows]

    async def list_by_rebanho(self, rebanho_id: UUID) -> list[Animal]:
        stmt = select(AnimalModel).where(AnimalModel.rebanho_id == rebanho_id)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(model) for model in rows]

    async def list_by_filtros(self, *, tipo: TipoAnimal | None=None, status: StatusAnimal | None=None) -> list[Animal]:
        stmt = select(AnimalModel)
        if tipo:
            stmt = stmt.where(AnimalModel.tipo == tipo.value)
        if status:
            stmt = stmt.where(AnimalModel.status == status.value)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(model) for model in rows]

    async def next_brinco(self, propriedade_id: UUID) -> str:
        ano = date.today().year
        prefix = str(propriedade_id)[:8]
        stmt = select(func.count()).select_from(AnimalModel).where(AnimalModel.brinco.like(f'{prefix}/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}/{ano}/{count + 1:04d}'

    @staticmethod
    def _to_domain(model: AnimalModel) -> Animal:
        return Animal(id=model.id, brinco=model.brinco, nome=model.nome, tipo=TipoAnimal(model.tipo), raca_id=model.raca_id, sexo=Sexo(model.sexo), data_nascimento=model.data_nascimento, peso_nascimento=model.peso_nascimento, peso_atual=model.peso_atual, status=StatusAnimal(model.status), proprietario_id=model.proprietario_id, propriedade_id=model.propriedade_id, rebanho_id=model.rebanho_id, mae_id=model.mae_id, pai_id=model.pai_id, data_entrada=model.data_entrada, data_saida=model.data_saida, observacoes=model.observacoes)