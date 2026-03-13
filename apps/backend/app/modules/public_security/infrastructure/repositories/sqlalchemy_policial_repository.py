from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.public_security.application.ports.policial_repository_port import PolicialRepositoryPort
from app.modules.public_security.domain.enums import CargoPolicial, Patente, StatusAgente, TipoAgente, TipoVinculo
from app.modules.public_security.domain.models.policial import Policial
from app.modules.public_security.infrastructure.models.policial_model import PolicialModel

class SQLAlchemyPolicialRepository(PolicialRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, policial: Policial) -> Policial:
        model = await self.session.get(PolicialModel, policial.id)
        if not model:
            model = PolicialModel(id=policial.id)
            self.session.add(model)
        model.matricula = policial.matricula
        model.unidade_id = policial.unidade_id
        model.nome = policial.nome
        model.data_nascimento = policial.data_nascimento
        model.cpf = policial.cpf
        model.rg = policial.rg
        model.tipo = policial.tipo.value
        model.vinculo = policial.vinculo.value
        model.cargo = policial.cargo.value if policial.cargo else None
        model.patente = policial.patente.value if policial.patente else None
        model.data_ingresso = policial.data_ingresso
        model.status = policial.status.value
        model.porte_arma = policial.porte_arma
        model.numero_porte = policial.numero_porte
        model.data_validade_porte = policial.data_validade_porte
        model.telefone = policial.telefone
        model.email = policial.email
        model.endereco = policial.endereco
        model.observacoes = policial.observacoes
        model.ativo = policial.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, policial_id: UUID) -> Policial | None:
        model = await self.session.get(PolicialModel, policial_id)
        return self._to_domain(model) if model else None

    async def get_by_matricula(self, matricula: str) -> Policial | None:
        stmt = select(PolicialModel).where(PolicialModel.matricula == matricula.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_cpf(self, cpf: str) -> Policial | None:
        stmt = select(PolicialModel).where(PolicialModel.cpf == cpf.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Policial]:
        stmt = select(PolicialModel).order_by(PolicialModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_unidade(self, unidade_id: UUID) -> list[Policial]:
        stmt = select(PolicialModel).where(PolicialModel.unidade_id == unidade_id).order_by(PolicialModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoAgente) -> list[Policial]:
        stmt = select(PolicialModel).where(PolicialModel.tipo == tipo.value).order_by(PolicialModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusAgente) -> list[Policial]:
        stmt = select(PolicialModel).where(PolicialModel.status == status.value).order_by(PolicialModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, policial_id: UUID) -> bool:
        model = await self.session.get(PolicialModel, policial_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_matricula(self, unidade_id: UUID) -> str:
        year = date.today().year
        unidade_fragmento = str(unidade_id).split('-')[0].upper()
        prefix = f'POL/{unidade_fragmento}/{year}/'
        stmt = select(func.count()).select_from(PolicialModel).where(PolicialModel.matricula.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:05d}'

    @staticmethod
    def _to_domain(model: PolicialModel) -> Policial:
        return Policial(id=model.id, matricula=model.matricula, unidade_id=model.unidade_id, nome=model.nome, data_nascimento=model.data_nascimento, cpf=model.cpf, rg=model.rg, tipo=TipoAgente(model.tipo), vinculo=TipoVinculo(model.vinculo), cargo=CargoPolicial(model.cargo) if model.cargo else None, patente=Patente(model.patente) if model.patente else None, data_ingresso=model.data_ingresso, status=StatusAgente(model.status), porte_arma=model.porte_arma, numero_porte=model.numero_porte, data_validade_porte=model.data_validade_porte, telefone=model.telefone, email=model.email, endereco=model.endereco, observacoes=model.observacoes, ativo=model.ativo)