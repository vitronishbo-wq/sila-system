from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.economy.trade.external.application.ports import (
    ImportadorRepositoryPort,
)
from apps.backend.app.modules.economy.trade.external.domain.enums import (
    RegimeImportacao,
    StatusHabilitacao,
    TipoOperador,
    TipoPessoa,
)
from apps.backend.app.modules.economy.trade.external.domain.models import Importador
from apps.backend.app.modules.economy.trade.external.infrastructure.models import ImportadorModel


class SQLAlchemyImportadorRepository(ImportadorRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, importador: Importador) -> Importador:
        model = await self.session.get(ImportadorModel, importador.id)
        if not model:
            model = ImportadorModel(id=importador.id)
            self.session.add(model)
        model.cadastro_radar = importador.cadastro_radar
        model.tipo_operador = importador.tipo_operador.value
        model.tipo_pessoa = importador.tipo_pessoa.value
        model.status = importador.status.value
        model.razao_social = importador.razao_social
        model.nome_fantasia = importador.nome_fantasia
        model.cnpj_cpf = importador.cnpj_cpf
        model.inscricao_estadual = importador.inscricao_estadual
        model.inscricao_municipal = importador.inscricao_municipal
        model.endereco = importador.endereco
        model.numero = importador.numero
        model.complemento = importador.complemento
        model.bairro = importador.bairro
        model.municipio = importador.municipio
        model.provincia = importador.provincia
        model.cep = importador.cep
        model.pais = importador.pais
        model.telefone = importador.telefone
        model.email = importador.email
        model.site = importador.site
        model.representante_nome = importador.representante_nome
        model.representante_cpf = importador.representante_cpf
        model.representante_cargo = importador.representante_cargo
        model.responsavel_nome = importador.responsavel_nome
        model.responsavel_cpf = importador.responsavel_cpf
        model.responsavel_registro = importador.responsavel_registro
        model.data_habilitacao = importador.data_habilitacao
        model.data_validade = importador.data_validade
        model.data_suspensao = importador.data_suspensao
        model.data_cancelamento = importador.data_cancelamento
        model.motivo_cancelamento = importador.motivo_cancelamento
        model.regimes_autorizados = [item.value for item in importador.regimes_autorizados]
        model.produtos_principais = (
            list(importador.produtos_principais)
            if importador.produtos_principais is not None
            else None
        )
        model.paises_origem = (
            list(importador.paises_origem) if importador.paises_origem is not None else None
        )
        model.banco_principal = importador.banco_principal
        model.conta_corrente = importador.conta_corrente
        model.swift_code = importador.swift_code
        model.limite_credito = importador.limite_credito
        model.observacoes = importador.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, id: UUID) -> Importador | None:
        model = await self.session.get(ImportadorModel, id)
        return self._to_domain(model) if model else None

    async def get_by_cnpj_cpf(self, cnpj_cpf: str) -> Importador | None:
        stmt = select(ImportadorModel).where(ImportadorModel.cnpj_cpf == cnpj_cpf.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list(
        self, *, status: StatusHabilitacao | None = None, municipio: str | None = None
    ) -> list[Importador]:
        stmt = select(ImportadorModel)
        if status is not None:
            stmt = stmt.where(ImportadorModel.status == status.value)
        if municipio is not None:
            stmt = stmt.where(ImportadorModel.municipio == municipio)
        stmt = stmt.order_by(ImportadorModel.razao_social.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    @staticmethod
    def _to_domain(model: ImportadorModel) -> Importador:
        return Importador(
            id=model.id,
            cadastro_radar=model.cadastro_radar,
            tipo_operador=TipoOperador(model.tipo_operador),
            tipo_pessoa=TipoPessoa(model.tipo_pessoa),
            status=StatusHabilitacao(model.status),
            razao_social=model.razao_social,
            nome_fantasia=model.nome_fantasia,
            cnpj_cpf=model.cnpj_cpf,
            inscricao_estadual=model.inscricao_estadual,
            inscricao_municipal=model.inscricao_municipal,
            endereco=model.endereco,
            numero=model.numero,
            complemento=model.complemento,
            bairro=model.bairro,
            municipio=model.municipio,
            provincia=model.provincia,
            cep=model.cep,
            pais=model.pais,
            telefone=model.telefone,
            email=model.email,
            site=model.site,
            representante_nome=model.representante_nome,
            representante_cpf=model.representante_cpf,
            representante_cargo=model.representante_cargo,
            responsavel_nome=model.responsavel_nome,
            responsavel_cpf=model.responsavel_cpf,
            responsavel_registro=model.responsavel_registro,
            data_habilitacao=model.data_habilitacao,
            data_validade=model.data_validade,
            data_suspensao=model.data_suspensao,
            data_cancelamento=model.data_cancelamento,
            motivo_cancelamento=model.motivo_cancelamento,
            regimes_autorizados=[
                RegimeImportacao(item) for item in model.regimes_autorizados or []
            ],
            produtos_principais=list(model.produtos_principais)
            if model.produtos_principais is not None
            else None,
            paises_origem=list(model.paises_origem) if model.paises_origem is not None else None,
            banco_principal=model.banco_principal,
            conta_corrente=model.conta_corrente,
            swift_code=model.swift_code,
            limite_credito=model.limite_credito,
            observacoes=model.observacoes,
        )
