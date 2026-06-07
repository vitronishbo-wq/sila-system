from __future__ import annotations

from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.modules.society.juventude.application.ports.jovem_repository_port import (
    JovemRepositoryPort,
)
from apps.backend.app.modules.society.juventude.domain.enums import (
    Escolaridade,
    FaixaEtaria,
    SituacaoOcupacional,
    TipoVulnerabilidade,
)
from apps.backend.app.modules.society.juventude.domain.models.jovem import Jovem
from apps.backend.app.modules.society.juventude.infrastructure.models.jovem_model import JovemModel


class SQLAlchemyJovemRepository(JovemRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, jovem: Jovem) -> Jovem:
        model = await self.session.get(JovemModel, jovem.id)
        if not model:
            model = JovemModel(id=jovem.id)
            self.session.add(model)
        model.numero_registro = jovem.numero_registro
        model.nome = jovem.nome
        model.data_nascimento = jovem.data_nascimento
        model.faixa_etaria = jovem.faixa_etaria.value
        model.genero = jovem.genero
        model.naturalidade = jovem.naturalidade
        model.nacionalidade = jovem.nacionalidade
        model.escolaridade = jovem.escolaridade.value
        model.situacao_ocupacional = jovem.situacao_ocupacional.value
        model.endereco = jovem.endereco
        model.municipio = jovem.municipio
        model.provincia = jovem.provincia
        model.telefone = jovem.telefone
        model.email = jovem.email
        model.citizen_id = jovem.citizen_id
        model.vulnerabilidades = (
            [item.value for item in jovem.vulnerabilidades] if jovem.vulnerabilidades else None
        )
        model.programas = jovem.programas
        model.auxilios = jovem.auxilios
        model.formacoes = jovem.formacoes
        model.experiencias = jovem.experiencias
        model.interesses = jovem.interesses
        model.habilidades = jovem.habilidades
        model.encaminhamentos = jovem.encaminhamentos
        model.acompanhamento_psicossocial = jovem.acompanhamento_psicossocial
        model.data_cadastro = jovem.data_cadastro
        model.observacoes = jovem.observacoes
        model.ativo = jovem.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, jovem_id: UUID) -> Jovem | None:
        model = await self.session.get(JovemModel, jovem_id)
        return self._to_domain(model) if model else None

    async def get_by_registro(self, numero_registro: str) -> Jovem | None:
        stmt = select(JovemModel).where(JovemModel.numero_registro == numero_registro.strip())
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def get_by_citizen(self, citizen_id: UUID) -> Jovem | None:
        stmt = select(JovemModel).where(JovemModel.citizen_id == citizen_id)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[Jovem]:
        stmt = select(JovemModel).order_by(JovemModel.nome.asc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_faixa_etaria(self, faixa_etaria: FaixaEtaria) -> list[Jovem]:
        stmt = (
            select(JovemModel)
            .where(JovemModel.faixa_etaria == faixa_etaria.value)
            .order_by(JovemModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_escolaridade(self, escolaridade: Escolaridade) -> list[Jovem]:
        stmt = (
            select(JovemModel)
            .where(JovemModel.escolaridade == escolaridade.value)
            .order_by(JovemModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_situacao(self, situacao: SituacaoOcupacional) -> list[Jovem]:
        stmt = (
            select(JovemModel)
            .where(JovemModel.situacao_ocupacional == situacao.value)
            .order_by(JovemModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_municipio(self, municipio: str) -> list[Jovem]:
        normalized = municipio.strip().lower()
        stmt = (
            select(JovemModel)
            .where(func.lower(JovemModel.municipio) == normalized)
            .order_by(JovemModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_vulneraveis(self) -> list[Jovem]:
        stmt = (
            select(JovemModel)
            .where(func.array_length(JovemModel.vulnerabilidades, 1) > 0)
            .order_by(JovemModel.nome.asc())
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def delete(self, jovem_id: UUID) -> bool:
        model = await self.session.get(JovemModel, jovem_id)
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def next_registro(self) -> str:
        ano = date.today().year
        stmt = (
            select(func.count())
            .select_from(JovemModel)
            .where(JovemModel.numero_registro.like(f"JOV/{ano}/%"))
        )
        count = (await self.session.execute(stmt)).scalar() or 0
        return f"JOV/{ano}/{count + 1:05d}"

    @staticmethod
    def _to_domain(model: JovemModel) -> Jovem:
        return Jovem(
            id=model.id,
            numero_registro=model.numero_registro,
            nome=model.nome,
            data_nascimento=model.data_nascimento,
            faixa_etaria=FaixaEtaria(model.faixa_etaria),
            genero=model.genero,
            naturalidade=model.naturalidade,
            nacionalidade=model.nacionalidade,
            escolaridade=Escolaridade(model.escolaridade),
            situacao_ocupacional=SituacaoOcupacional(model.situacao_ocupacional),
            endereco=model.endereco,
            municipio=model.municipio,
            provincia=model.provincia,
            telefone=model.telefone,
            email=model.email,
            citizen_id=model.citizen_id,
            vulnerabilidades=[TipoVulnerabilidade(item) for item in model.vulnerabilidades]
            if model.vulnerabilidades
            else None,
            programas=model.programas,
            auxilios=model.auxilios,
            formacoes=model.formacoes,
            experiencias=model.experiencias,
            interesses=model.interesses,
            habilidades=model.habilidades,
            encaminhamentos=model.encaminhamentos,
            acompanhamento_psicossocial=model.acompanhamento_psicossocial,
            data_cadastro=model.data_cadastro,
            observacoes=model.observacoes,
            ativo=model.ativo,
        )
