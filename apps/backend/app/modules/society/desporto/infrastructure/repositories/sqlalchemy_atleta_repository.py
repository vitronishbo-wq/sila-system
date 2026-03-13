from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.desporto.application.ports.atleta_repository_port import AtletaRepositoryPort
from apps.backend.app.modules.society.desporto.domain.enums import ModalidadeDesportiva, PePreferencial, PosicaoAtleta, StatusAtleta, TipoAtleta
from apps.backend.app.modules.society.desporto.domain.models.atleta import Atleta
from apps.backend.app.modules.society.desporto.infrastructure.models.atleta_model import AtletaModel

class SQLAlchemyAtletaRepository(AtletaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, atleta: Atleta) -> Atleta:
        model = await self.session.get(AtletaModel, atleta.id)
        if not model:
            model = AtletaModel(id=atleta.id)
            self.session.add(model)
        model.numero_registro = atleta.numero_registro
        model.nome = atleta.nome
        model.data_nascimento = atleta.data_nascimento
        model.naturalidade = atleta.naturalidade
        model.nacionalidade = atleta.nacionalidade
        model.tipo = atleta.tipo.value
        model.modalidades = [item.value for item in atleta.modalidades]
        model.status = atleta.status.value
        model.posicoes = [item.value for item in atleta.posicoes] if atleta.posicoes else None
        model.pe_preferencial = atleta.pe_preferencial.value if atleta.pe_preferencial else None
        model.altura_cm = atleta.altura_cm
        model.peso_kg = atleta.peso_kg
        model.clube_atual_id = atleta.clube_atual_id
        model.numero_camisola = atleta.numero_camisola
        model.citizen_id = atleta.citizen_id
        model.ultimo_exame_id = atleta.ultimo_exame_id
        model.data_cadastro = atleta.data_cadastro
        model.ativo = atleta.ativo
        model.observacoes = atleta.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, atleta_id: UUID) -> Atleta | None:
        model = await self.session.get(AtletaModel, atleta_id)
        return self._to_domain(model) if model else None

    async def get_by_registro(self, numero_registro: str) -> Atleta | None:
        stmt = select(AtletaModel).where(AtletaModel.numero_registro == numero_registro.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: UUID) -> Atleta | None:
        stmt = select(AtletaModel).where(AtletaModel.citizen_id == citizen_id)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Atleta]:
        stmt = select(AtletaModel).order_by(AtletaModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_clube(self, clube_id: UUID) -> list[Atleta]:
        stmt = select(AtletaModel).where(AtletaModel.clube_atual_id == clube_id).order_by(AtletaModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_modalidade(self, modalidade: ModalidadeDesportiva) -> list[Atleta]:
        stmt = select(AtletaModel).where(AtletaModel.modalidades.contains([modalidade.value])).order_by(AtletaModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusAtleta) -> list[Atleta]:
        stmt = select(AtletaModel).where(AtletaModel.status == status.value).order_by(AtletaModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoAtleta) -> list[Atleta]:
        stmt = select(AtletaModel).where(AtletaModel.tipo == tipo.value).order_by(AtletaModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, atleta_id: UUID) -> bool:
        model = await self.session.get(AtletaModel, atleta_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_registro(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(AtletaModel).where(AtletaModel.numero_registro.like(f'ATL/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'ATL/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: AtletaModel) -> Atleta:
        return Atleta(id=model.id, numero_registro=model.numero_registro, nome=model.nome, data_nascimento=model.data_nascimento, naturalidade=model.naturalidade, nacionalidade=model.nacionalidade, tipo=TipoAtleta(model.tipo), modalidades=[ModalidadeDesportiva(item) for item in model.modalidades], data_cadastro=model.data_cadastro, status=StatusAtleta(model.status), posicoes=[PosicaoAtleta(item) for item in model.posicoes] if model.posicoes else None, pe_preferencial=PePreferencial(model.pe_preferencial) if model.pe_preferencial else None, altura_cm=model.altura_cm, peso_kg=model.peso_kg, clube_atual_id=model.clube_atual_id, numero_camisola=model.numero_camisola, citizen_id=model.citizen_id, ultimo_exame_id=model.ultimo_exame_id, observacoes=model.observacoes, ativo=model.ativo)