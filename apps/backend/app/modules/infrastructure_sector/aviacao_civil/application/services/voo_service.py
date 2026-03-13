from __future__ import annotations
from datetime import datetime
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.events import VooDecoladoEvent, VooPousadoEvent, VooProgramadoEvent, event_bus
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.ports.aeronave_repository_port import AeronaveRepositoryPort
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.application.ports.voo_repository_port import VooRepositoryPort
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.enums import NaturezaVoo, RegrasVoo, StatusAeronavegabilidade, StatusVoo, TipoVoo
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.domain.models.voo import Voo
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.adapters.decea_adapter import DeceaAdapter
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.adapters.meteorologia_adapter import MeteorologiaAdapter
from apps.backend.app.modules.infrastructure_sector.aviacao_civil.infrastructure.persistence.outbox import InMemoryOutbox

class VooService:

    def __init__(self, *, voo_repo: VooRepositoryPort, aeronave_repo: AeronaveRepositoryPort, outbox: InMemoryOutbox, decea_adapter: DeceaAdapter | None=None, meteorologia_adapter: MeteorologiaAdapter | None=None) -> None:
        self.voo_repo = voo_repo
        self.aeronave_repo = aeronave_repo
        self.outbox = outbox
        self.decea = decea_adapter
        self.meteorologia = meteorologia_adapter

    async def programar_voo(self, *, numero_voo: str, empresa_id: UUID, aeronave_id: UUID, aeroporto_origem_id: UUID, aeroporto_destino_id: UUID, data_hora_partida: datetime, data_hora_chegada: datetime, tipo: TipoVoo, natureza: NaturezaVoo, regras: RegrasVoo, passageiros: int, tripulantes: list[dict]) -> Voo:
        aeronave = await self.aeronave_repo.get_by_id(aeronave_id)
        if aeronave is None:
            raise ValueError('Aeronave nao encontrada')
        if aeronave.status_aeronavegabilidade != StatusAeronavegabilidade.VALIDO:
            raise ValueError('Aeronave sem aeronavegabilidade valida')
        voo = Voo(numero_voo=numero_voo, empresa_id=empresa_id, aeronave_id=aeronave_id, aeroporto_origem_id=aeroporto_origem_id, aeroporto_destino_id=aeroporto_destino_id, data_hora_partida_programada=data_hora_partida, data_hora_chegada_programada=data_hora_chegada, tipo=tipo, natureza=natureza, regras=regras, passageiros=passageiros, tripulantes=tripulantes)
        await self.voo_repo.save(voo)
        evento = VooProgramadoEvent(voo_id=voo.id, numero_voo=voo.numero_voo, empresa_id=empresa_id, aeronave_id=aeronave_id, origem=aeroporto_origem_id, destino=aeroporto_destino_id, partida_programada=data_hora_partida)
        await self.outbox.append(evento)
        await event_bus.publish(evento)
        if self.decea is not None:
            await self.decea.registrar_voo({'numero_voo': voo.numero_voo, 'aeronave_id': str(aeronave_id), 'origem': str(aeroporto_origem_id), 'destino': str(aeroporto_destino_id)})
        if self.meteorologia is not None:
            await self.meteorologia.consultar_rota(origem=aeroporto_origem_id, destino=aeroporto_destino_id, data_hora=data_hora_partida)
        return voo

    async def registrar_decolagem(self, *, voo_id: UUID, data_hora: datetime) -> Voo:
        voo = await self.voo_repo.get_by_id(voo_id)
        if voo is None:
            raise ValueError('Voo nao encontrado')
        atraso = voo.registrar_partida(data_hora)
        await self.voo_repo.save(voo)
        evento = VooDecoladoEvent(voo_id=voo.id, numero_voo=voo.numero_voo, data_hora=data_hora, atraso_minutos=atraso)
        await self.outbox.append(evento)
        await event_bus.publish(evento)
        return voo

    async def registrar_pouso(self, *, voo_id: UUID, data_hora: datetime) -> Voo:
        voo = await self.voo_repo.get_by_id(voo_id)
        if voo is None:
            raise ValueError('Voo nao encontrado')
        tempo_voo = voo.registrar_chegada(data_hora)
        await self.voo_repo.save(voo)
        aeronave = await self.aeronave_repo.get_by_id(voo.aeronave_id)
        if aeronave is not None and tempo_voo > 0:
            aeronave.registrar_voo(tempo_voo)
            await self.aeronave_repo.save(aeronave)
        evento = VooPousadoEvent(voo_id=voo.id, numero_voo=voo.numero_voo, data_hora=data_hora, tempo_voo_horas=tempo_voo)
        await self.outbox.append(evento)
        await event_bus.publish(evento)
        return voo

    async def get_voos_ativos(self) -> list[Voo]:
        return await self.voo_repo.find_by_status(StatusVoo.EM_VOO)

    async def get_estatisticas_dia(self, *, data: datetime) -> dict:
        inicio = data.replace(hour=0, minute=0, second=0, microsecond=0)
        fim = data.replace(hour=23, minute=59, second=59, microsecond=999999)
        voos = await self.voo_repo.find_by_periodo(inicio, fim)
        return {'data': data.date().isoformat(), 'total_voos': len(voos), 'por_status': {status.value: len([item for item in voos if item.status == status]) for status in StatusVoo}, 'passageiros_total': sum((item.passageiros for item in voos))}