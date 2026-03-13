from __future__ import annotations
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.application.ports.operadora_repository_port import OperadoraRepositoryPort
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusOutorga, TipoOperadora, TipoServico
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.domain.models.operadora import Operadora
from apps.backend.app.modules.infrastructure_sector.telecomunicacoes.infrastructure.models.operadora_model import OperadoraModel

class SQLAlchemyOperadoraRepository(OperadoraRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, operadora: Operadora) -> Operadora:
        model = await self.session.get(OperadoraModel, operadora.id)
        if not model:
            model = OperadoraModel(id=operadora.id)
            self.session.add(model)
        model.cnpj = operadora.cnpj
        model.razao_social = operadora.razao_social
        model.nome_fantasia = operadora.nome_fantasia
        model.tipo = operadora.tipo.value
        model.servicos_autorizados = [item.value for item in operadora.servicos_autorizados]
        model.endereco = operadora.endereco
        model.municipio = operadora.municipio
        model.provincia = operadora.provincia
        model.telefone = operadora.telefone
        model.email = operadora.email
        model.representante_legal = operadora.representante_legal
        model.representante_documento = operadora.representante_documento
        model.representante_cargo = operadora.representante_cargo
        model.outorga_id = operadora.outorga_id
        model.data_autorizacao = operadora.data_autorizacao
        model.data_validade = operadora.data_validade
        model.status = operadora.status.value
        model.observacoes = operadora.observacoes
        model.ativo = operadora.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, operadora_id: UUID) -> Operadora | None:
        model = await self.session.get(OperadoraModel, operadora_id)
        return self._to_domain(model) if model else None

    async def get_by_cnpj(self, cnpj: str) -> Operadora | None:
        stmt = select(OperadoraModel).where(OperadoraModel.cnpj == cnpj.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Operadora]:
        stmt = select(OperadoraModel).order_by(OperadoraModel.razao_social.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_servico(self, servico: TipoServico) -> list[Operadora]:
        stmt = select(OperadoraModel).where(OperadoraModel.servicos_autorizados.contains([servico.value])).order_by(OperadoraModel.razao_social.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[Operadora]:
        normalized = municipio.strip().lower()
        stmt = select(OperadoraModel).where(func.lower(OperadoraModel.municipio) == normalized).order_by(OperadoraModel.razao_social.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_ativas(self) -> list[Operadora]:
        stmt = select(OperadoraModel).where(OperadoraModel.ativo.is_(True), OperadoraModel.status.in_([StatusOutorga.DEFERIDA.value, StatusOutorga.RENOVADA.value])).order_by(OperadoraModel.razao_social.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, operadora_id: UUID) -> bool:
        model = await self.session.get(OperadoraModel, operadora_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    @staticmethod
    def _to_domain(model: OperadoraModel) -> Operadora:
        return Operadora(id=model.id, cnpj=model.cnpj, razao_social=model.razao_social, nome_fantasia=model.nome_fantasia, tipo=TipoOperadora(model.tipo), servicos_autorizados=[TipoServico(item) for item in model.servicos_autorizados], endereco=model.endereco, municipio=model.municipio, provincia=model.provincia, telefone=model.telefone, email=model.email, representante_legal=model.representante_legal, representante_documento=model.representante_documento, representante_cargo=model.representante_cargo, outorga_id=model.outorga_id, data_autorizacao=model.data_autorizacao, data_validade=model.data_validade, status=StatusOutorga(model.status), observacoes=model.observacoes, ativo=model.ativo)