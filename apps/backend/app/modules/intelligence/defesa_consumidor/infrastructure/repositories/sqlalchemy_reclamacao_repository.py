from __future__ import annotations
from datetime import datetime
from typing import Any
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.intelligence.defesa_consumidor.application.ports.reclamacao_repository_port import ReclamacaoRepositoryPort
from app.modules.intelligence.defesa_consumidor.infrastructure.models.reclamacao_model import ReclamacaoModel

class SQLAlchemyReclamacaoRepository(ReclamacaoRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        model = ReclamacaoModel(**data)
        self.session.add(model)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_dict()

    async def get_by_id(self, reclamacao_id: int) -> dict[str, Any] | None:
        result = await self.session.execute(select(ReclamacaoModel).where(ReclamacaoModel.id == reclamacao_id))
        model = result.scalars().first()
        return model.to_dict() if model else None

    async def get_by_protocolo(self, protocolo: str) -> dict[str, Any] | None:
        result = await self.session.execute(select(ReclamacaoModel).where(ReclamacaoModel.protocolo == protocolo))
        model = result.scalars().first()
        return model.to_dict() if model else None

    async def list_by_consumidor(self, consumidor_id: int, limit: int=50, offset: int=0) -> list[dict[str, Any]]:
        result = await self.session.execute(select(ReclamacaoModel).where(ReclamacaoModel.consumidor_id == consumidor_id).order_by(ReclamacaoModel.data_abertura.desc()).limit(limit).offset(offset))
        return [item.to_dict() for item in result.scalars().all()]

    async def list_by_estabelecimento(self, estabelecimento_id: int, limit: int=50, offset: int=0) -> list[dict[str, Any]]:
        result = await self.session.execute(select(ReclamacaoModel).where(ReclamacaoModel.estabelecimento_id == estabelecimento_id).order_by(ReclamacaoModel.data_abertura.desc()).limit(limit).offset(offset))
        return [item.to_dict() for item in result.scalars().all()]

    async def list_by_status(self, status: str, limit: int=100, offset: int=0) -> list[dict[str, Any]]:
        result = await self.session.execute(select(ReclamacaoModel).where(ReclamacaoModel.status == status).order_by(ReclamacaoModel.data_abertura.desc()).limit(limit).offset(offset))
        return [item.to_dict() for item in result.scalars().all()]

    async def list_by_periodo(self, data_inicio: datetime, data_fim: datetime) -> list[dict[str, Any]]:
        result = await self.session.execute(select(ReclamacaoModel).where(and_(ReclamacaoModel.data_abertura >= data_inicio, ReclamacaoModel.data_abertura <= data_fim)).order_by(ReclamacaoModel.data_abertura.desc()))
        return [item.to_dict() for item in result.scalars().all()]

    async def list_prioritarias(self, prioridade: str, limit: int=50) -> list[dict[str, Any]]:
        result = await self.session.execute(select(ReclamacaoModel).where(and_(ReclamacaoModel.prioridade == prioridade, ReclamacaoModel.resolvido.is_(False))).order_by(ReclamacaoModel.data_abertura.asc()).limit(limit))
        return [item.to_dict() for item in result.scalars().all()]

    async def update(self, data: dict[str, Any]) -> dict[str, Any]:
        result = await self.session.execute(select(ReclamacaoModel).where(ReclamacaoModel.id == data['id']))
        model = result.scalars().first()
        if not model:
            raise ValueError(f'Reclamacao {data['id']} nao encontrada')
        for key, value in data.items():
            if key != 'id' and hasattr(model, key) and (value is not None):
                setattr(model, key, value)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_dict()

    async def delete(self, reclamacao_id: int) -> bool:
        result = await self.session.execute(select(ReclamacaoModel).where(ReclamacaoModel.id == reclamacao_id))
        model = result.scalars().first()
        if not model:
            return False
        await self.session.delete(model)
        await self.session.commit()
        return True

    async def count_by_status(self, status: str) -> int:
        result = await self.session.execute(select(func.count(ReclamacaoModel.id)).where(ReclamacaoModel.status == status))
        return int(result.scalar() or 0)

    async def count_total(self) -> int:
        result = await self.session.execute(select(func.count(ReclamacaoModel.id)))
        return int(result.scalar() or 0)