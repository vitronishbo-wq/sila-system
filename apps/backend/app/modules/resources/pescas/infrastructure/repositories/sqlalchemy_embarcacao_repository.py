from __future__ import annotations
from datetime import date
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.backend.app.modules.resources.pescas.application.ports import EmbarcacaoRepositoryPort
from apps.backend.app.modules.resources.pescas.domain.enums import ModalidadePesca, TipoEmbarcacao
from apps.backend.app.modules.resources.pescas.domain.models.embarcacao import Embarcacao
from apps.backend.app.modules.resources.pescas.infrastructure.models.embarcacao_model import EmbarcacaoModel

class SQLAlchemyEmbarcacaoRepository(EmbarcacaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, embarcacao: Embarcacao) -> Embarcacao:
        model = await self.session.get(EmbarcacaoModel, embarcacao.id)
        if not model:
            model = EmbarcacaoModel(id=embarcacao.id)
            self.session.add(model)
        model.nome = embarcacao.nome
        model.numero_inscricao = embarcacao.numero_inscricao
        model.tipo = embarcacao.tipo.value
        model.modalidades = [m.value for m in embarcacao.modalidades]
        model.comprimento = embarcacao.comprimento
        model.arqueacao_bruta = embarcacao.arqueacao_bruta
        model.potencia_motor = embarcacao.potencia_motor
        model.capacidade_porao = embarcacao.capacidade_porao
        model.tripulacao_minima = embarcacao.tripulacao_minima
        model.porto_registro = embarcacao.porto_registro
        model.ano_construcao = embarcacao.ano_construcao
        model.material_casco = embarcacao.material_casco
        model.proprietario_id = embarcacao.proprietario_id
        model.armador_id = embarcacao.armador_id
        model.licenca_id = embarcacao.licenca_id
        model.sistema_rastreio = embarcacao.sistema_rastreio
        model.data_inspecao = embarcacao.data_inspecao
        model.data_validade_doc = embarcacao.data_validade_doc
        model.observacoes = embarcacao.observacoes
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_domain(model)

    async def get_by_id(self, embarcacao_id: UUID) -> Embarcacao | None:
        model = await self.session.get(EmbarcacaoModel, embarcacao_id)
        return self._to_domain(model) if model else None

    async def get_by_inscricao(self, numero_inscricao: str) -> Embarcacao | None:
        stmt = select(EmbarcacaoModel).where(EmbarcacaoModel.numero_inscricao == numero_inscricao)
        model = (await self.session.execute(stmt)).scalars().first()
        return self._to_domain(model) if model else None

    async def list_by_proprietario(self, proprietario_id: UUID) -> list[Embarcacao]:
        stmt = select(EmbarcacaoModel).where(EmbarcacaoModel.proprietario_id == proprietario_id)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def list_by_tipo(self, tipo: TipoEmbarcacao) -> list[Embarcacao]:
        stmt = select(EmbarcacaoModel).where(EmbarcacaoModel.tipo == tipo.value)
        rows = (await self.session.execute(stmt)).scalars().all()
        return [self._to_domain(row) for row in rows]

    async def next_inscricao(self, porto: str) -> str:
        ano = date.today().year
        stmt = select(func.count()).select_from(EmbarcacaoModel).where(EmbarcacaoModel.numero_inscricao.like(f'{porto}/{ano}/%'))
        count = (await self.session.execute(stmt)).scalar() or 0
        return f'{porto}/{ano}/{count + 1:04d}'

    @staticmethod
    def _to_domain(model: EmbarcacaoModel) -> Embarcacao:
        return Embarcacao(id=model.id, nome=model.nome, numero_inscricao=model.numero_inscricao, tipo=TipoEmbarcacao(model.tipo), modalidades=[ModalidadePesca(item) for item in model.modalidades], comprimento=model.comprimento, arqueacao_bruta=model.arqueacao_bruta, potencia_motor=model.potencia_motor, capacidade_porao=model.capacidade_porao, tripulacao_minima=model.tripulacao_minima, porto_registro=model.porto_registro, ano_construcao=model.ano_construcao, material_casco=model.material_casco, proprietario_id=model.proprietario_id, armador_id=model.armador_id, licenca_id=model.licenca_id, sistema_rastreio=model.sistema_rastreio, data_inspecao=model.data_inspecao, data_validade_doc=model.data_validade_doc, observacoes=model.observacoes)