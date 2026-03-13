from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.society.cultura.application.ports.patrimonio_imaterial_repository_port import PatrimonioImaterialRepositoryPort
from apps.backend.app.modules.society.cultura.domain.enums import CategoriaPatrimonioImaterial, StatusPatrimonioImaterial
from apps.backend.app.modules.society.cultura.domain.models.patrimonio_imaterial import PatrimonioImaterial
from apps.backend.app.modules.society.cultura.infrastructure.models.patrimonio_imaterial_model import PatrimonioImaterialModel

class SQLAlchemyPatrimonioImaterialRepository(PatrimonioImaterialRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, patrimonio: PatrimonioImaterial) -> PatrimonioImaterial:
        model = await self.session.get(PatrimonioImaterialModel, patrimonio.id)
        if not model:
            model = PatrimonioImaterialModel(id=patrimonio.id)
            self.session.add(model)
        model.registro_pni = patrimonio.registro_pni
        model.nome = patrimonio.nome
        model.categoria = patrimonio.categoria.value
        model.descricao = patrimonio.descricao
        model.comunidade = patrimonio.comunidade
        model.municipio = patrimonio.municipio
        model.provincia = patrimonio.provincia
        model.status = patrimonio.status.value
        model.atracao_turistica_id = patrimonio.atracao_turistica_id
        model.instituicao_educacional_id = patrimonio.instituicao_educacional_id
        model.plano_salvaguarda = patrimonio.plano_salvaguarda
        model.data_registro = patrimonio.data_registro
        model.ativo = patrimonio.ativo
        model.observacoes = patrimonio.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, patrimonio_id: UUID) -> PatrimonioImaterial | None:
        model = await self.session.get(PatrimonioImaterialModel, patrimonio_id)
        return self._to_domain(model) if model else None

    async def get_by_registro(self, registro_pni: str) -> PatrimonioImaterial | None:
        stmt = select(PatrimonioImaterialModel).where(PatrimonioImaterialModel.registro_pni == registro_pni.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[PatrimonioImaterial]:
        stmt = select(PatrimonioImaterialModel).order_by(PatrimonioImaterialModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_categoria(self, categoria: CategoriaPatrimonioImaterial) -> list[PatrimonioImaterial]:
        stmt = select(PatrimonioImaterialModel).where(PatrimonioImaterialModel.categoria == categoria.value).order_by(PatrimonioImaterialModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[PatrimonioImaterial]:
        stmt = select(PatrimonioImaterialModel).where(func.lower(PatrimonioImaterialModel.municipio) == municipio.strip().lower()).order_by(PatrimonioImaterialModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_status(self, status: StatusPatrimonioImaterial) -> list[PatrimonioImaterial]:
        stmt = select(PatrimonioImaterialModel).where(PatrimonioImaterialModel.status == status.value).order_by(PatrimonioImaterialModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, patrimonio_id: UUID) -> bool:
        model = await self.session.get(PatrimonioImaterialModel, patrimonio_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_registro(self) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(PatrimonioImaterialModel).where(PatrimonioImaterialModel.registro_pni.like(f'PIM/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'PIM/{ano}/{count + 1:05d}'

    @staticmethod
    def _to_domain(model: PatrimonioImaterialModel) -> PatrimonioImaterial:
        return PatrimonioImaterial(id=model.id, registro_pni=model.registro_pni, nome=model.nome, categoria=CategoriaPatrimonioImaterial(model.categoria), descricao=model.descricao, comunidade=model.comunidade, municipio=model.municipio, provincia=model.provincia, data_registro=model.data_registro, status=StatusPatrimonioImaterial(model.status), atracao_turistica_id=model.atracao_turistica_id, instituicao_educacional_id=model.instituicao_educacional_id, plano_salvaguarda=model.plano_salvaguarda, ativo=model.ativo, observacoes=model.observacoes)