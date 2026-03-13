from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.society.juventude.application.ports.risco_evasao_repository_port import RiscoEvasaoRepositoryPort
from app.modules.society.juventude.domain.enums import RiscoSocial, SituacaoOcupacional, TipoVulnerabilidade
from app.modules.society.juventude.domain.models.risco_evasao import RiscoEvasao
from app.modules.society.juventude.infrastructure.models.risco_evasao_model import RiscoEvasaoModel

class SQLAlchemyRiscoEvasaoRepository(RiscoEvasaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, risco: RiscoEvasao) -> RiscoEvasao:
        model = await self.session.get(RiscoEvasaoModel, risco.id)
        if not model:
            model = RiscoEvasaoModel(id=risco.id)
            self.session.add(model)
        model.codigo_risco = risco.codigo_risco
        model.jovem_id = risco.jovem_id
        model.citizen_id = risco.citizen_id
        model.matricula_ativa = risco.matricula_ativa
        model.situacao_ocupacional = risco.situacao_ocupacional.value
        model.vulnerabilidades = [item.value for item in risco.vulnerabilidades] if risco.vulnerabilidades else None
        model.pontuacao = risco.pontuacao
        model.nivel_risco = risco.nivel_risco.value
        model.data_avaliacao = risco.data_avaliacao
        model.fatores = risco.fatores
        model.recomendacoes = risco.recomendacoes
        model.observacoes = risco.observacoes
        model.ativo = risco.ativo
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, risco_id: UUID) -> RiscoEvasao | None:
        model = await self.session.get(RiscoEvasaoModel, risco_id)
        return self._to_domain(model) if model else None

    async def get_ativo_by_jovem(self, jovem_id: UUID) -> RiscoEvasao | None:
        stmt = select(RiscoEvasaoModel).where(RiscoEvasaoModel.jovem_id == jovem_id, RiscoEvasaoModel.ativo.is_(True)).order_by(RiscoEvasaoModel.data_avaliacao.desc()).limit(1)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_all(self) -> list[RiscoEvasao]:
        stmt = select(RiscoEvasaoModel).order_by(RiscoEvasaoModel.data_avaliacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def list_by_nivel(self, nivel: RiscoSocial) -> list[RiscoEvasao]:
        stmt = select(RiscoEvasaoModel).where(RiscoEvasaoModel.nivel_risco == nivel.value).order_by(RiscoEvasaoModel.data_avaliacao.desc())
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(item) for item in rows]

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'RISK/{year}/'
        stmt = select(func.count()).select_from(RiscoEvasaoModel).where(RiscoEvasaoModel.codigo_risco.like(f'{prefix}%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{prefix}{count + 1:05d}'

    @staticmethod
    def _to_domain(model: RiscoEvasaoModel) -> RiscoEvasao:
        return RiscoEvasao(id=model.id, codigo_risco=model.codigo_risco, jovem_id=model.jovem_id, citizen_id=model.citizen_id, matricula_ativa=model.matricula_ativa, situacao_ocupacional=SituacaoOcupacional(model.situacao_ocupacional), vulnerabilidades=[TipoVulnerabilidade(item) for item in model.vulnerabilidades] if model.vulnerabilidades else None, pontuacao=model.pontuacao, nivel_risco=RiscoSocial(model.nivel_risco), data_avaliacao=model.data_avaliacao, fatores=list(model.fatores or []), recomendacoes=list(model.recomendacoes or []), observacoes=model.observacoes, ativo=model.ativo)