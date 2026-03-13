from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.society.desporto.application.ports.atleta_repository_port import AtletaRepositoryPort
from app.modules.society.desporto.application.ports.clube_repository_port import ClubeRepositoryPort
from app.modules.society.desporto.application.ports.competicao_repository_port import CompeticaoRepositoryPort
from app.modules.society.desporto.application.ports.educacao_service_port import EducacaoServicePort
from app.modules.society.desporto.application.ports.estadio_repository_port import EstadioRepositoryPort
from app.modules.society.desporto.application.ports.obras_publicas_service_port import ObrasPublicasServicePort
from app.modules.society.desporto.application.ports.outbox_repository_port import OutboxRepositoryPort
from app.modules.society.desporto.application.ports.request_service_port import RequestServicePort
from app.modules.society.desporto.application.ports.saude_service_port import SaudeServicePort
from app.modules.society.desporto.application.ports.turismo_service_port import TurismoServicePort
from app.modules.society.desporto.domain.enums import ModalidadeDesportiva, StatusJogo, StatusAtleta, StatusCompeticao, TipoClube, TipoAtleta, TipoCompeticao
from app.modules.society.desporto.domain.models.atleta import Atleta
from app.modules.society.desporto.domain.models.clube import Clube
from app.modules.society.desporto.domain.models.competicao import Competicao
from app.modules.society.desporto.domain.models.estadio import Estadio
from app.modules.society.desporto.domain.models.jogo import Jogo
from app.modules.society.desporto.application.ports.jogo_repository_port import JogoRepositoryPort

class InMemoryAtletaRepository(AtletaRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Atleta] = {}

    async def save(self, atleta: Atleta) -> Atleta:
        self._items[atleta.id] = atleta
        return atleta

    async def get_by_id(self, atleta_id: UUID) -> Atleta | None:
        return self._items.get(atleta_id)

    async def get_by_registro(self, numero_registro: str) -> Atleta | None:
        normalized = numero_registro.strip()
        for item in self._items.values():
            if item.numero_registro == normalized:
                return item
        return None

    async def get_by_citizen(self, citizen_id: UUID) -> Atleta | None:
        for item in self._items.values():
            if item.citizen_id == citizen_id:
                return item
        return None

    async def list_all(self) -> list[Atleta]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_clube(self, clube_id: UUID) -> list[Atleta]:
        values = [item for item in self._items.values() if item.clube_atual_id == clube_id]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_modalidade(self, modalidade: ModalidadeDesportiva) -> list[Atleta]:
        values = [item for item in self._items.values() if modalidade in item.modalidades]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_status(self, status: StatusAtleta) -> list[Atleta]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_tipo(self, tipo: TipoAtleta) -> list[Atleta]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: item.nome)

    async def delete(self, atleta_id: UUID) -> bool:
        return self._items.pop(atleta_id, None) is not None

    async def next_registro(self) -> str:
        year = date.today().year
        prefix = f'ATL/{year}/'
        count = sum((1 for item in self._items.values() if item.numero_registro.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryCompeticaoRepository(CompeticaoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Competicao] = {}

    async def save(self, competicao: Competicao) -> Competicao:
        self._items[competicao.id] = competicao
        return competicao

    async def get_by_id(self, competicao_id: UUID) -> Competicao | None:
        return self._items.get(competicao_id)

    async def get_by_codigo(self, codigo_competicao: str) -> Competicao | None:
        normalized = codigo_competicao.strip()
        for item in self._items.values():
            if item.codigo_competicao == normalized:
                return item
        return None

    async def list_all(self) -> list[Competicao]:
        return sorted(self._items.values(), key=lambda item: (item.data_inicio, item.nome))

    async def list_by_tipo(self, tipo: TipoCompeticao) -> list[Competicao]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: (item.data_inicio, item.nome))

    async def list_by_modalidade(self, modalidade: ModalidadeDesportiva) -> list[Competicao]:
        values = [item for item in self._items.values() if item.modalidade == modalidade]
        return sorted(values, key=lambda item: (item.data_inicio, item.nome))

    async def list_by_status(self, status: StatusCompeticao) -> list[Competicao]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: (item.data_inicio, item.nome))

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[Competicao]:
        values = [item for item in self._items.values() if item.data_inicio >= data_inicio and item.data_fim <= data_fim]
        return sorted(values, key=lambda item: (item.data_inicio, item.nome))

    async def delete(self, competicao_id: UUID) -> bool:
        return self._items.pop(competicao_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'CMP/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_competicao.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryClubeRepository(ClubeRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Clube] = {}

    async def save(self, clube: Clube) -> Clube:
        self._items[clube.id] = clube
        return clube

    async def get_by_id(self, clube_id: UUID) -> Clube | None:
        return self._items.get(clube_id)

    async def get_by_codigo(self, codigo_clube: str) -> Clube | None:
        normalized = codigo_clube.strip()
        for item in self._items.values():
            if item.codigo_clube == normalized:
                return item
        return None

    async def list_all(self) -> list[Clube]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_tipo(self, tipo: TipoClube) -> list[Clube]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_modalidade(self, modalidade: ModalidadeDesportiva) -> list[Clube]:
        values = [item for item in self._items.values() if item.modalidade_principal == modalidade]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_municipio(self, municipio: str) -> list[Clube]:
        normalized = municipio.strip().lower()
        values = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(values, key=lambda item: item.nome)

    async def delete(self, clube_id: UUID) -> bool:
        return self._items.pop(clube_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'CLB/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_clube.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryJogoRepository(JogoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Jogo] = {}

    async def save(self, jogo: Jogo) -> Jogo:
        self._items[jogo.id] = jogo
        return jogo

    async def get_by_id(self, jogo_id: UUID) -> Jogo | None:
        return self._items.get(jogo_id)

    async def get_by_codigo(self, codigo_jogo: str) -> Jogo | None:
        normalized = codigo_jogo.strip()
        for item in self._items.values():
            if item.codigo_jogo == normalized:
                return item
        return None

    async def list_all(self) -> list[Jogo]:
        return sorted(self._items.values(), key=lambda item: (item.data_jogo, item.codigo_jogo))

    async def list_by_competicao(self, competicao_id: UUID) -> list[Jogo]:
        values = [item for item in self._items.values() if item.competicao_id == competicao_id]
        return sorted(values, key=lambda item: (item.data_jogo, item.codigo_jogo))

    async def list_by_clube(self, clube_id: UUID) -> list[Jogo]:
        values = [item for item in self._items.values() if item.clube_casa_id == clube_id or item.clube_fora_id == clube_id]
        return sorted(values, key=lambda item: (item.data_jogo, item.codigo_jogo))

    async def list_by_status(self, status: StatusJogo) -> list[Jogo]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: (item.data_jogo, item.codigo_jogo))

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[Jogo]:
        values = [item for item in self._items.values() if item.data_jogo >= data_inicio and item.data_jogo <= data_fim]
        return sorted(values, key=lambda item: (item.data_jogo, item.codigo_jogo))

    async def delete(self, jogo_id: UUID) -> bool:
        return self._items.pop(jogo_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'JOG/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_jogo.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryEstadioRepository(EstadioRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Estadio] = {}

    async def save(self, estadio: Estadio) -> Estadio:
        self._items[estadio.id] = estadio
        return estadio

    async def get_by_id(self, estadio_id: UUID) -> Estadio | None:
        return self._items.get(estadio_id)

    async def get_by_codigo(self, codigo_estadio: str) -> Estadio | None:
        normalized = codigo_estadio.strip()
        for item in self._items.values():
            if item.codigo_estadio == normalized:
                return item
        return None

    async def list_all(self) -> list[Estadio]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_municipio(self, municipio: str) -> list[Estadio]:
        normalized = municipio.strip().lower()
        values = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(values, key=lambda item: item.nome)

    async def delete(self, estadio_id: UUID) -> bool:
        return self._items.pop(estadio_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'EST/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_estadio.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryOutboxRepository(OutboxRepositoryPort):

    def __init__(self) -> None:
        self.events: list[object] = []

    async def append(self, event: object) -> None:
        self.events.append(event)

    async def pop_batch(self, batch_size: int=100) -> list[object]:
        if batch_size <= 0:
            return []
        batch = self.events[:batch_size]
        self.events = self.events[batch_size:]
        return batch

class FakeEventBus:

    def __init__(self) -> None:
        self.events: list[object] = []

    async def publish(self, event: object) -> None:
        self.events.append(event)

class FakeCitizenService:

    def __init__(self, *, active: bool=True) -> None:
        self.active = active

    async def is_citizen_active(self, citizen_id: UUID) -> bool:
        return self.active

class FakeSaudeService(SaudeServicePort):

    def __init__(self, *, exists: bool=True) -> None:
        self.exists = exists

    async def exame_exists(self, exame_id: UUID) -> bool:
        return self.exists

class FakeTurismoService(TurismoServicePort):

    def __init__(self, *, exists: bool=True) -> None:
        self.exists = exists

    async def atracao_exists(self, atracao_id: UUID) -> bool:
        return self.exists

class FakeEducacaoService(EducacaoServicePort):

    def __init__(self, *, exists: bool=True) -> None:
        self.exists = exists

    async def instituicao_exists(self, instituicao_id: UUID) -> bool:
        return self.exists

class FakeObrasPublicasService(ObrasPublicasServicePort):

    def __init__(self, *, exists: bool=True) -> None:
        self.exists = exists

    async def obra_exists(self, codigo_obra: str) -> bool:
        return self.exists

class FakeRequestService(RequestServicePort):

    async def create_request(self, *, request_type: str, entity_id: UUID, metadata: dict | None=None, citizen_id: UUID | None=None, numero_processo: str | None=None) -> UUID | None:
        return None