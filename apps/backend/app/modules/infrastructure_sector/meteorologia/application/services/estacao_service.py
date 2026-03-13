from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from uuid import UUID
from app.modules.infrastructure_sector.meteorologia.application.ports.estacao_repository_port import EstacaoRepositoryPort
from app.modules.infrastructure_sector.meteorologia.domain.enums import StationStatus
from app.modules.infrastructure_sector.meteorologia.domain.models import EstacaoMeteorologica

class EstacaoService:

    def __init__(self, estacao_repository: EstacaoRepositoryPort) -> None:
        self.estacao_repository = estacao_repository

    async def criar_estacao(self, payload: dict[str, Any]) -> EstacaoMeteorologica:
        codigo = str(payload['codigo']).strip().upper()
        existente = await self.estacao_repository.get_by_codigo(codigo)
        if existente is not None:
            raise ValueError(f'Ja existe estacao com codigo {codigo}')
        estacao = EstacaoMeteorologica(codigo=codigo, nome=payload['nome'], latitude=payload['latitude'], longitude=payload['longitude'], altitude=payload.get('altitude'), municipio=payload.get('municipio'), provincia=payload.get('provincia'), metadata=payload.get('metadata') or {}, status=StationStatus.ACTIVE)
        estacao.update_location(latitude=payload['latitude'], longitude=payload['longitude'], altitude=payload.get('altitude'))
        return await self.estacao_repository.save(estacao)

    async def obter_estacao(self, estacao_id: UUID) -> EstacaoMeteorologica:
        estacao = await self.estacao_repository.get_by_id(estacao_id)
        if estacao is None:
            raise ValueError('Estacao nao encontrada')
        return estacao

    async def listar_estacoes(self, *, provincia: str | None=None, status: str | None=None, limit: int=100, offset: int=0) -> list[EstacaoMeteorologica]:
        status_enum: StationStatus | None = None
        if status:
            try:
                status_enum = StationStatus(status.upper())
            except ValueError as exc:
                raise ValueError(f'Status invalido: {status}') from exc
        return await self.estacao_repository.list_filtered(provincia=provincia, status=status_enum, limit=limit, offset=offset)

    async def atualizar_estacao(self, estacao_id: UUID, payload: dict[str, Any]) -> EstacaoMeteorologica:
        estacao = await self.obter_estacao(estacao_id)
        if 'nome' in payload and payload['nome'] is not None:
            estacao.nome = payload['nome']
        if 'municipio' in payload and payload['municipio'] is not None:
            estacao.municipio = payload['municipio']
        if 'provincia' in payload and payload['provincia'] is not None:
            estacao.provincia = payload['provincia']
        if 'metadata' in payload and payload['metadata'] is not None:
            estacao.metadata = payload['metadata']
        if any((key in payload and payload[key] is not None for key in ('latitude', 'longitude', 'altitude'))):
            latitude = payload.get('latitude', estacao.latitude)
            longitude = payload.get('longitude', estacao.longitude)
            altitude = payload.get('altitude', estacao.altitude)
            if latitude is None or longitude is None:
                raise ValueError('Latitude e longitude sao obrigatorias para atualizar localizacao')
            estacao.update_location(latitude=latitude, longitude=longitude, altitude=altitude)
        status = payload.get('status')
        if status is not None:
            try:
                estacao.status = StationStatus(str(status).upper())
            except ValueError as exc:
                raise ValueError(f'Status invalido: {status}') from exc
        estacao.updated_at = datetime.now(timezone.utc)
        return await self.estacao_repository.save(estacao)

    async def remover_estacao(self, estacao_id: UUID) -> None:
        removida = await self.estacao_repository.delete(estacao_id)
        if not removida:
            raise ValueError('Estacao nao encontrada')