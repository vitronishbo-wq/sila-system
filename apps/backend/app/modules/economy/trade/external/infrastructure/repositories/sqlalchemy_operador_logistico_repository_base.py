from __future__ import annotations
from typing import Generic, TypeVar
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import OperadorLogisticoRepositoryPort
from app.modules.economy.trade.external.domain.enums import StatusHabilitacao, TipoOperador, TipoPessoa
from app.modules.economy.trade.external.domain.models import OperadorLogisticoBase
from app.modules.economy.trade.external.infrastructure.models.operador_logistico_columns_mixin import OperadorLogisticoColumnsMixin
TOperadorLogistico = TypeVar('TOperadorLogistico', bound=OperadorLogisticoBase)
TOperadorLogisticoModel = TypeVar('TOperadorLogisticoModel', bound=OperadorLogisticoColumnsMixin)

class SQLAlchemyOperadorLogisticoRepositoryBase(OperadorLogisticoRepositoryPort[TOperadorLogistico], Generic[TOperadorLogistico, TOperadorLogisticoModel]):

    def __init__(self, session: AsyncSession, *, model_cls: type[TOperadorLogisticoModel], domain_cls: type[TOperadorLogistico]) -> None:
        self.session = session
        self._model_cls = model_cls
        self._domain_cls = domain_cls

    async def save(self, operador: TOperadorLogistico) -> TOperadorLogistico:
        model = await self.session.get(self._model_cls, operador.id)
        if not model:
            model = self._model_cls(id=operador.id)
            self.session.add(model)
        model.cadastro_radar = operador.cadastro_radar
        model.tipo_operador = operador.tipo_operador.value
        model.tipo_pessoa = operador.tipo_pessoa.value
        model.status = operador.status.value
        model.razao_social = operador.razao_social
        model.nome_fantasia = operador.nome_fantasia
        model.cnpj_cpf = operador.cnpj_cpf
        model.endereco = operador.endereco
        model.numero = operador.numero
        model.complemento = operador.complemento
        model.bairro = operador.bairro
        model.municipio = operador.municipio
        model.provincia = operador.provincia
        model.cep = operador.cep
        model.pais = operador.pais
        model.telefone = operador.telefone
        model.email = operador.email
        model.site = operador.site
        model.numero_licenca = operador.numero_licenca
        model.orgao_anuente = operador.orgao_anuente
        model.data_habilitacao = operador.data_habilitacao
        model.data_validade = operador.data_validade
        model.data_suspensao = operador.data_suspensao
        model.data_cancelamento = operador.data_cancelamento
        model.motivo_cancelamento = operador.motivo_cancelamento
        model.observacoes = operador.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> TOperadorLogistico | None:
        model = await self.session.get(self._model_cls, id)
        return self._to_domain(model) if model else None

    async def get_by_cnpj_cpf(self, cnpj_cpf: str) -> TOperadorLogistico | None:
        stmt = select(self._model_cls).where(self._model_cls.cnpj_cpf == cnpj_cpf.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list(self, *, status: StatusHabilitacao | None=None, municipio: str | None=None) -> list[TOperadorLogistico]:
        stmt = select(self._model_cls)
        if status is not None:
            stmt = stmt.where(self._model_cls.status == status.value)
        if municipio is not None:
            stmt = stmt.where(self._model_cls.municipio == municipio)
        stmt = stmt.order_by(self._model_cls.razao_social.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    def _to_domain(self, model: TOperadorLogisticoModel) -> TOperadorLogistico:
        return self._domain_cls(id=model.id, cadastro_radar=model.cadastro_radar, tipo_operador=TipoOperador(model.tipo_operador), tipo_pessoa=TipoPessoa(model.tipo_pessoa), status=StatusHabilitacao(model.status), razao_social=model.razao_social, cnpj_cpf=model.cnpj_cpf, endereco=model.endereco, numero=model.numero, bairro=model.bairro, municipio=model.municipio, provincia=model.provincia, cep=model.cep, nome_fantasia=model.nome_fantasia, complemento=model.complemento, pais=model.pais, telefone=model.telefone, email=model.email, site=model.site, numero_licenca=model.numero_licenca, orgao_anuente=model.orgao_anuente, data_habilitacao=model.data_habilitacao, data_validade=model.data_validade, data_suspensao=model.data_suspensao, data_cancelamento=model.data_cancelamento, motivo_cancelamento=model.motivo_cancelamento, observacoes=model.observacoes)