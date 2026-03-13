from __future__ import annotations
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.economy.trade.external.application.ports import ExportadorRepositoryPort
from app.modules.economy.trade.external.domain.enums import RegimeExportacao, StatusHabilitacao, TipoOperador, TipoPessoa
from app.modules.economy.trade.external.domain.models import Exportador
from app.modules.economy.trade.external.infrastructure.models import ExportadorModel

class SQLAlchemyExportadorRepository(ExportadorRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, exportador: Exportador) -> Exportador:
        model = await self.session.get(ExportadorModel, exportador.id)
        if not model:
            model = ExportadorModel(id=exportador.id)
            self.session.add(model)
        model.cadastro_radar = exportador.cadastro_radar
        model.tipo_operador = exportador.tipo_operador.value
        model.tipo_pessoa = exportador.tipo_pessoa.value
        model.status = exportador.status.value
        model.razao_social = exportador.razao_social
        model.nome_fantasia = exportador.nome_fantasia
        model.cnpj_cpf = exportador.cnpj_cpf
        model.inscricao_estadual = exportador.inscricao_estadual
        model.inscricao_municipal = exportador.inscricao_municipal
        model.endereco = exportador.endereco
        model.numero = exportador.numero
        model.complemento = exportador.complemento
        model.bairro = exportador.bairro
        model.municipio = exportador.municipio
        model.provincia = exportador.provincia
        model.cep = exportador.cep
        model.pais = exportador.pais
        model.telefone = exportador.telefone
        model.email = exportador.email
        model.site = exportador.site
        model.representante_nome = exportador.representante_nome
        model.representante_cpf = exportador.representante_cpf
        model.representante_cargo = exportador.representante_cargo
        model.responsavel_nome = exportador.responsavel_nome
        model.responsavel_cpf = exportador.responsavel_cpf
        model.responsavel_registro = exportador.responsavel_registro
        model.data_habilitacao = exportador.data_habilitacao
        model.data_validade = exportador.data_validade
        model.data_suspensao = exportador.data_suspensao
        model.data_cancelamento = exportador.data_cancelamento
        model.motivo_cancelamento = exportador.motivo_cancelamento
        model.regimes_autorizados = [item.value for item in exportador.regimes_autorizados]
        model.produtos_principais = list(exportador.produtos_principais) if exportador.produtos_principais is not None else None
        model.paises_destino = list(exportador.paises_destino) if exportador.paises_destino is not None else None
        model.banco_principal = exportador.banco_principal
        model.conta_corrente = exportador.conta_corrente
        model.swift_code = exportador.swift_code
        model.limite_credito = exportador.limite_credito
        model.observacoes = exportador.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> Exportador | None:
        model = await self.session.get(ExportadorModel, id)
        return self._to_domain(model) if model else None

    async def get_by_cnpj_cpf(self, cnpj_cpf: str) -> Exportador | None:
        stmt = select(ExportadorModel).where(ExportadorModel.cnpj_cpf == cnpj_cpf.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list(self, *, status: StatusHabilitacao | None=None, municipio: str | None=None) -> list[Exportador]:
        stmt = select(ExportadorModel)
        if status is not None:
            stmt = stmt.where(ExportadorModel.status == status.value)
        if municipio is not None:
            stmt = stmt.where(ExportadorModel.municipio == municipio)
        stmt = stmt.order_by(ExportadorModel.razao_social.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    @staticmethod
    def _to_domain(model: ExportadorModel) -> Exportador:
        return Exportador(id=model.id, cadastro_radar=model.cadastro_radar, tipo_operador=TipoOperador(model.tipo_operador), tipo_pessoa=TipoPessoa(model.tipo_pessoa), status=StatusHabilitacao(model.status), razao_social=model.razao_social, nome_fantasia=model.nome_fantasia, cnpj_cpf=model.cnpj_cpf, inscricao_estadual=model.inscricao_estadual, inscricao_municipal=model.inscricao_municipal, endereco=model.endereco, numero=model.numero, complemento=model.complemento, bairro=model.bairro, municipio=model.municipio, provincia=model.provincia, cep=model.cep, pais=model.pais, telefone=model.telefone, email=model.email, site=model.site, representante_nome=model.representante_nome, representante_cpf=model.representante_cpf, representante_cargo=model.representante_cargo, responsavel_nome=model.responsavel_nome, responsavel_cpf=model.responsavel_cpf, responsavel_registro=model.responsavel_registro, data_habilitacao=model.data_habilitacao, data_validade=model.data_validade, data_suspensao=model.data_suspensao, data_cancelamento=model.data_cancelamento, motivo_cancelamento=model.motivo_cancelamento, regimes_autorizados=[RegimeExportacao(item) for item in model.regimes_autorizados or []], produtos_principais=list(model.produtos_principais) if model.produtos_principais is not None else None, paises_destino=list(model.paises_destino) if model.paises_destino is not None else None, banco_principal=model.banco_principal, conta_corrente=model.conta_corrente, swift_code=model.swift_code, limite_credito=model.limite_credito, observacoes=model.observacoes)