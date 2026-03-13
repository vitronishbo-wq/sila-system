from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.civil_protection.application.ports.bombeiro_repository_port import BombeiroRepositoryPort
from apps.backend.app.modules.civil_protection.domain.enums import CargoBombeiro, StatusAgenteProtecao, TipoAgenteProtecao
from apps.backend.app.modules.civil_protection.domain.models.bombeiro import Bombeiro
from apps.backend.app.modules.civil_protection.infrastructure.models.bombeiro_model import BombeiroModel

class SQLAlchemyBombeiroRepository(BombeiroRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, bombeiro: Bombeiro) -> Bombeiro:
        model = await self.session.get(BombeiroModel, bombeiro.id)
        if not model:
            model = BombeiroModel(id=bombeiro.id)
            self.session.add(model)
        model.matricula = bombeiro.matricula
        model.corporacao_id = bombeiro.corporacao_id
        model.nome = bombeiro.nome
        model.data_nascimento = bombeiro.data_nascimento
        model.cpf = bombeiro.cpf
        model.rg = bombeiro.rg
        model.tipo = bombeiro.tipo.value
        model.cargo = bombeiro.cargo.value if bombeiro.cargo else None
        model.data_ingresso = bombeiro.data_ingresso
        model.status = bombeiro.status.value
        model.telefone = bombeiro.telefone
        model.email = bombeiro.email
        model.endereco = bombeiro.endereco
        model.observacoes = bombeiro.observacoes
        model.ativo = bombeiro.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, bombeiro_id: UUID) -> Bombeiro | None:
        model = await self.session.get(BombeiroModel, bombeiro_id)
        return self._to_domain(model) if model else None

    async def get_by_matricula(self, matricula: str) -> Bombeiro | None:
        stmt = select(BombeiroModel).where(BombeiroModel.matricula == matricula.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_cpf(self, cpf: str) -> Bombeiro | None:
        stmt = select(BombeiroModel).where(BombeiroModel.cpf == cpf.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Bombeiro]:
        stmt = select(BombeiroModel).order_by(BombeiroModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_corporacao(self, corporacao_id: UUID) -> list[Bombeiro]:
        stmt = select(BombeiroModel).where(BombeiroModel.corporacao_id == corporacao_id).order_by(BombeiroModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusAgenteProtecao) -> list[Bombeiro]:
        stmt = select(BombeiroModel).where(BombeiroModel.status == status.value).order_by(BombeiroModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, bombeiro_id: UUID) -> bool:
        model = await self.session.get(BombeiroModel, bombeiro_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_matricula(self, corporacao_id: UUID) -> str:
        year = date.today().year
        fragment = str(corporacao_id).split('-')[0].upper()
        prefix = f'BOM/{fragment}/{year}/'
        stmt = select(func.count()).select_from(BombeiroModel).where(BombeiroModel.matricula.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:05d}'

    @staticmethod
    def _to_domain(model: BombeiroModel) -> Bombeiro:
        return Bombeiro(id=model.id, matricula=model.matricula, corporacao_id=model.corporacao_id, nome=model.nome, data_nascimento=model.data_nascimento, cpf=model.cpf, rg=model.rg, tipo=TipoAgenteProtecao(model.tipo), cargo=CargoBombeiro(model.cargo) if model.cargo else None, data_ingresso=model.data_ingresso, status=StatusAgenteProtecao(model.status), telefone=model.telefone, email=model.email, endereco=model.endereco, observacoes=model.observacoes, ativo=model.ativo)