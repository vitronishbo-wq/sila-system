from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.society.cultura.application.events import EventoProgramadoEvent, event_bus
from apps.backend.app.modules.society.cultura.application.ports.artista_repository_port import ArtistaRepositoryPort
from apps.backend.app.modules.society.cultura.application.ports.educacao_service_port import EducacaoServicePort
from apps.backend.app.modules.society.cultura.application.ports.evento_cultural_repository_port import EventoCulturalRepositoryPort
from apps.backend.app.modules.society.cultura.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.society.cultura.application.ports.turismo_service_port import TurismoServicePort
from apps.backend.app.modules.society.cultura.domain.enums import StatusEventoCultural, TipoEventoCultural
from apps.backend.app.modules.society.cultura.domain.models.evento_cultural import EventoCultural

class EventoCulturalService:

    def __init__(self, *, evento_repo: EventoCulturalRepositoryPort, artista_repo: ArtistaRepositoryPort, turismo_service: TurismoServicePort | None=None, educacao_service: EducacaoServicePort | None=None, request_service: RequestServicePort | None=None) -> None:
        self.evento_repo = evento_repo
        self.artista_repo = artista_repo
        self.turismo_service = turismo_service
        self.educacao_service = educacao_service
        self.request_service = request_service

    async def cadastrar_evento(self, *, nome: str, tipo: TipoEventoCultural, descricao: str, data_inicio: date, data_fim: date, local: str, municipio: str, provincia: str, realizador_id: UUID, atracao_turistica_id: UUID | None=None, instituicao_educacional_id: UUID | None=None, entrada_gratuita: bool=True, valor_ingresso: Decimal | None=None, publico_estimado: int | None=None, observacoes: str | None=None) -> EventoCultural:
        realizador = await self.artista_repo.get_by_id(realizador_id)
        if realizador is None:
            raise ValueError('Artista realizador nao encontrado')
        await self._validar_integracoes(atracao_turistica_id=atracao_turistica_id, instituicao_educacional_id=instituicao_educacional_id)
        codigo = await self.evento_repo.next_codigo()
        evento = EventoCultural.criar(codigo_evento=codigo, nome=nome, tipo=tipo, descricao=descricao, data_inicio=data_inicio, data_fim=data_fim, local=local, municipio=municipio, provincia=provincia, realizador_id=realizador_id, atracao_turistica_id=atracao_turistica_id, instituicao_educacional_id=instituicao_educacional_id, entrada_gratuita=entrada_gratuita, valor_ingresso=valor_ingresso, publico_estimado=publico_estimado, observacoes=observacoes)
        saved = await self.evento_repo.save(evento)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_EVENTO_CULTURAL', entity_id=saved.id, citizen_id=realizador.citizen_id, metadata={'codigo_evento': saved.codigo_evento, 'tipo': saved.tipo.value, 'municipio': saved.municipio}, numero_processo=saved.codigo_evento)
        await event_bus.publish(EventoProgramadoEvent(evento_id=saved.id, nome=saved.nome, tipo=saved.tipo.value, data_inicio=saved.data_inicio.isoformat(), data_fim=saved.data_fim.isoformat(), local=saved.local, capacidade=saved.publico_estimado or 0))
        return saved

    async def buscar_evento(self, evento_id: UUID) -> EventoCultural:
        item = await self.evento_repo.get_by_id(evento_id)
        if item is None:
            raise ValueError('Evento cultural nao encontrado')
        return item

    async def listar_eventos(self, *, tipo: TipoEventoCultural | None=None, municipio: str | None=None, status: StatusEventoCultural | None=None, data_inicio: date | None=None, data_fim: date | None=None, somente_ativos: bool=True) -> list[EventoCultural]:
        if tipo is not None:
            itens = await self.evento_repo.list_by_tipo(tipo)
        elif municipio is not None:
            itens = await self.evento_repo.list_by_municipio(municipio)
        elif status is not None:
            itens = await self.evento_repo.list_by_status(status)
        elif data_inicio is not None and data_fim is not None:
            itens = await self.evento_repo.list_by_periodo(data_inicio, data_fim)
        else:
            itens = await self.evento_repo.list_all()
        if somente_ativos:
            return [item for item in itens if item.ativo]
        return itens

    async def atualizar_evento(self, *, evento_id: UUID, nome: str | None=None, tipo: TipoEventoCultural | None=None, descricao: str | None=None, data_inicio: date | None=None, data_fim: date | None=None, local: str | None=None, municipio: str | None=None, provincia: str | None=None, atracao_turistica_id: UUID | None=None, instituicao_educacional_id: UUID | None=None, entrada_gratuita: bool | None=None, valor_ingresso: Decimal | None=None, publico_estimado: int | None=None, status: StatusEventoCultural | None=None, ativo: bool | None=None, observacoes: str | None=None) -> EventoCultural:
        item = await self.buscar_evento(evento_id)
        await self._validar_integracoes(atracao_turistica_id=atracao_turistica_id, instituicao_educacional_id=instituicao_educacional_id)
        item.atualizar(nome=nome, tipo=tipo, descricao=descricao, data_inicio=data_inicio, data_fim=data_fim, local=local, municipio=municipio, provincia=provincia, atracao_turistica_id=atracao_turistica_id, instituicao_educacional_id=instituicao_educacional_id, entrada_gratuita=entrada_gratuita, valor_ingresso=valor_ingresso, publico_estimado=publico_estimado, status=status, ativo=ativo, observacoes=observacoes)
        return await self.evento_repo.save(item)

    async def remover_evento(self, evento_id: UUID) -> None:
        deleted = await self.evento_repo.delete(evento_id)
        if not deleted:
            raise ValueError('Evento cultural nao encontrado')

    async def _validar_integracoes(self, *, atracao_turistica_id: UUID | None, instituicao_educacional_id: UUID | None) -> None:
        if atracao_turistica_id is not None and self.turismo_service is not None:
            existe = await self.turismo_service.atracao_exists(atracao_turistica_id)
            if not existe:
                raise ValueError('Atracao turistica nao encontrada')
        if instituicao_educacional_id is not None and self.educacao_service is not None:
            existe = await self.educacao_service.instituicao_exists(instituicao_educacional_id)
            if not existe:
                raise ValueError('Instituicao educacional nao encontrada')