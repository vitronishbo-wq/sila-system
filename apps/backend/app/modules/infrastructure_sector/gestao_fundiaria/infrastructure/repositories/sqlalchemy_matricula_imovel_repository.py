from __future__ import annotations
from datetime import date
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.matricula_imovel_repository_port import MatriculaImovelRepositoryPort
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusMatriculaImovel, TipoRegistro
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.matricula_imovel import MatriculaImovel
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.infrastructure.models.matricula_imovel_model import MatriculaImovelModel

class SQLAlchemyMatriculaImovelRepository(MatriculaImovelRepositoryPort):

    def __init__(self, session: AsyncSession | None=None) -> None:
        self._session = session
        self._items: dict[str, MatriculaImovel] = {}
        self._seq = 0

    async def save(self, item: MatriculaImovel) -> MatriculaImovel:
        if self._session:
            existing = await self._session.execute(select(MatriculaImovelModel).where(MatriculaImovelModel.numero_matricula == item.numero_matricula))
            model = existing.scalars().first()
            if model is None:
                model = MatriculaImovelModel(id=item.id, numero_matricula=item.numero_matricula, imovel_inscricao=item.imovel_inscricao, tipo_registro=item.tipo_registro.value, cartorio_nome=item.cartorio_nome, livro=item.livro, folha=item.folha, comarca=item.comarca, provincia=item.provincia, data_registro=item.data_registro, status=item.status.value, ativo=item.ativo, proprietario_documento=item.proprietario_documento, data_atualizacao=item.data_atualizacao, observacoes=item.observacoes)
                self._session.add(model)
            else:
                model.imovel_inscricao = item.imovel_inscricao
                model.tipo_registro = item.tipo_registro.value
                model.cartorio_nome = item.cartorio_nome
                model.livro = item.livro
                model.folha = item.folha
                model.comarca = item.comarca
                model.provincia = item.provincia
                model.status = item.status.value
                model.ativo = item.ativo
                model.proprietario_documento = item.proprietario_documento
                model.data_atualizacao = item.data_atualizacao
                model.observacoes = item.observacoes
            await self._session.flush()
            return self._to_domain(model)
        self._items[item.numero_matricula] = item
        return item

    async def get_by_numero(self, numero_matricula: str) -> MatriculaImovel | None:
        if self._session:
            result = await self._session.execute(select(MatriculaImovelModel).where(MatriculaImovelModel.numero_matricula == numero_matricula))
            model = result.scalars().first()
            return self._to_domain(model) if model else None
        return self._items.get(numero_matricula)

    async def list(self, *, imovel_inscricao: str | None=None, status: StatusMatriculaImovel | None=None, ativo: bool | None=None) -> list[MatriculaImovel]:
        if self._session:
            statement = select(MatriculaImovelModel)
            if imovel_inscricao:
                statement = statement.where(MatriculaImovelModel.imovel_inscricao == imovel_inscricao.strip())
            if status:
                statement = statement.where(MatriculaImovelModel.status == status.value)
            if ativo is not None:
                statement = statement.where(MatriculaImovelModel.ativo == ativo)
            result = await self._session.execute(statement.order_by(MatriculaImovelModel.numero_matricula.asc()))
            return [self._to_domain(model) for model in result.scalars().all()]
        values = list(self._items.values())
        if imovel_inscricao:
            values = [item for item in values if item.imovel_inscricao == imovel_inscricao.strip()]
        if status:
            values = [item for item in values if item.status == status]
        if ativo is not None:
            values = [item for item in values if item.ativo == ativo]
        return values

    async def next_numero(self) -> str:
        if self._session:
            year = date.today().year
            prefix = f'MAT/{year}/'
            result = await self._session.execute(select(func.count()).select_from(MatriculaImovelModel).where(MatriculaImovelModel.numero_matricula.like(f'{prefix}%')))
            seq = int(result.scalar() or 0) + 1
            return f'{prefix}{seq:06d}'
        self._seq += 1
        return f'MAT/{date.today().year}/{self._seq:06d}'

    @staticmethod
    def _to_domain(model: MatriculaImovelModel) -> MatriculaImovel:
        return MatriculaImovel(id=model.id, numero_matricula=model.numero_matricula, imovel_inscricao=model.imovel_inscricao, tipo_registro=TipoRegistro(model.tipo_registro), cartorio_nome=model.cartorio_nome, livro=model.livro, folha=model.folha, comarca=model.comarca, provincia=model.provincia, data_registro=model.data_registro, status=StatusMatriculaImovel(model.status), ativo=model.ativo, proprietario_documento=model.proprietario_documento, data_atualizacao=model.data_atualizacao, observacoes=model.observacoes)