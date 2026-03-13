from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.cultura.application.ports.artista_repository_port import ArtistaRepositoryPort
from apps.backend.app.modules.society.cultura.domain.enums import TipoArtista
from apps.backend.app.modules.society.cultura.domain.models.artista import Artista
from apps.backend.app.modules.society.cultura.infrastructure.models.artista_model import ArtistaModel

class SQLAlchemyArtistaRepository(ArtistaRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, artista: Artista) -> Artista:
        model = await self.session.get(ArtistaModel, artista.id)
        if not model:
            model = ArtistaModel(id=artista.id)
            self.session.add(model)
        model.registro_cultural = artista.registro_cultural
        model.nome = artista.nome
        model.nome_artistico = artista.nome_artistico
        model.tipo = [item.value for item in artista.tipo]
        model.data_nascimento = artista.data_nascimento
        model.naturalidade = artista.naturalidade
        model.nacionalidade = artista.nacionalidade
        model.biografia = artista.biografia
        model.citizen_id = artista.citizen_id
        model.municipio = artista.municipio
        model.provincia = artista.provincia
        model.data_cadastro = artista.data_cadastro
        model.ativo = artista.ativo
        model.observacoes = artista.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, artista_id: UUID) -> Artista | None:
        model = await self.session.get(ArtistaModel, artista_id)
        return self._to_domain(model) if model else None

    async def get_by_registro(self, registro_cultural: str) -> Artista | None:
        stmt = select(ArtistaModel).where(ArtistaModel.registro_cultural == registro_cultural.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Artista]:
        stmt = select(ArtistaModel).order_by(ArtistaModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_tipo(self, tipo: TipoArtista) -> list[Artista]:
        stmt = select(ArtistaModel).where(ArtistaModel.tipo.contains([tipo.value])).order_by(ArtistaModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, artista_id: UUID) -> bool:
        model = await self.session.get(ArtistaModel, artista_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_registro(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(ArtistaModel).where(ArtistaModel.registro_cultural.like(f'ART/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'ART/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: ArtistaModel) -> Artista:
        return Artista(id=model.id, registro_cultural=model.registro_cultural, nome=model.nome, tipo=[TipoArtista(item) for item in model.tipo], data_cadastro=model.data_cadastro, nome_artistico=model.nome_artistico, data_nascimento=model.data_nascimento, naturalidade=model.naturalidade, nacionalidade=model.nacionalidade, biografia=model.biografia, citizen_id=model.citizen_id, municipio=model.municipio, provincia=model.provincia, ativo=model.ativo, observacoes=model.observacoes)