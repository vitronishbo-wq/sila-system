from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from apps.backend.app.modules.society.cultura.application.ports.artista_repository_port import (
    ArtistaRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.bem_cultural_repository_port import (
    BemCulturalRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.edital_repository_port import (
    EditalRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.educacao_service_port import (
    EducacaoServicePort,
)
from apps.backend.app.modules.society.cultura.application.ports.espaco_cultural_repository_port import (
    EspacoCulturalRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.evento_cultural_repository_port import (
    EventoCulturalRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.grupo_artistico_repository_port import (
    GrupoArtisticoRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.patrimonio_imaterial_repository_port import (
    PatrimonioImaterialRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.projeto_cultural_repository_port import (
    ProjetoCulturalRepositoryPort,
)
from apps.backend.app.modules.society.cultura.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.cultura.application.ports.turismo_service_port import (
    TurismoServicePort,
)
from apps.backend.app.modules.society.cultura.domain.enums import (
    CategoriaPatrimonioImaterial,
    FaseEditalCultural,
    StatusEventoCultural,
    StatusPatrimonioImaterial,
    StatusProjetoCultural,
    StatusTombamento,
    TipoArtista,
    TipoEditalCultural,
    TipoEspacoCultural,
    TipoEventoCultural,
    TipoGrupoArtistico,
    TipoPatrimonio,
    TipoProjetoCultural,
)
from apps.backend.app.modules.society.cultura.domain.models.artista import Artista
from apps.backend.app.modules.society.cultura.domain.models.bem_cultural import BemCultural
from apps.backend.app.modules.society.cultura.domain.models.edital import Edital
from apps.backend.app.modules.society.cultura.domain.models.espaco_cultural import EspacoCultural
from apps.backend.app.modules.society.cultura.domain.models.evento_cultural import EventoCultural
from apps.backend.app.modules.society.cultura.domain.models.grupo_artistico import GrupoArtistico
from apps.backend.app.modules.society.cultura.domain.models.patrimonio_imaterial import (
    PatrimonioImaterial,
)
from apps.backend.app.modules.society.cultura.domain.models.projeto_cultural import ProjetoCultural


class InMemoryArtistaRepository(ArtistaRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Artista] = {}

    async def save(self, artista: Artista) -> Artista:
        self._items[artista.id] = artista
        return artista

    async def get_by_id(self, artista_id: UUID) -> Artista | None:
        return self._items.get(artista_id)

    async def get_by_registro(self, registro_cultural: str) -> Artista | None:
        normalized = registro_cultural.strip()
        for item in self._items.values():
            if item.registro_cultural == normalized:
                return item
        return None

    async def list_all(self) -> list[Artista]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_tipo(self, tipo: TipoArtista) -> list[Artista]:
        values = [item for item in self._items.values() if tipo in item.tipo]
        return sorted(values, key=lambda item: item.nome)

    async def delete(self, artista_id: UUID) -> bool:
        return self._items.pop(artista_id, None) is not None

    async def next_registro(self) -> str:
        year = date.today().year
        prefix = f"ART/{year}/"
        count = sum(1 for item in self._items.values() if item.registro_cultural.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryBemCulturalRepository(BemCulturalRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, BemCultural] = {}

    async def save(self, bem: BemCultural) -> BemCultural:
        self._items[bem.id] = bem
        return bem

    async def get_by_id(self, bem_id: UUID) -> BemCultural | None:
        return self._items.get(bem_id)

    async def get_by_registro(self, registro_ipat: str) -> BemCultural | None:
        normalized = registro_ipat.strip()
        for item in self._items.values():
            if item.registro_ipat == normalized:
                return item
        return None

    async def list_all(self) -> list[BemCultural]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_tipo(self, tipo: TipoPatrimonio) -> list[BemCultural]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_municipio(self, municipio: str) -> list[BemCultural]:
        normalized = municipio.strip().lower()
        values = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_status_tombamento(self, status: StatusTombamento) -> list[BemCultural]:
        values = [item for item in self._items.values() if item.status_tombamento == status]
        return sorted(values, key=lambda item: item.nome)

    async def delete(self, bem_id: UUID) -> bool:
        return self._items.pop(bem_id, None) is not None

    async def next_registro(self) -> str:
        year = date.today().year
        prefix = f"IPAT/{year}/"
        count = sum(1 for item in self._items.values() if item.registro_ipat.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryEventoCulturalRepository(EventoCulturalRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, EventoCultural] = {}

    async def save(self, evento: EventoCultural) -> EventoCultural:
        self._items[evento.id] = evento
        return evento

    async def get_by_id(self, evento_id: UUID) -> EventoCultural | None:
        return self._items.get(evento_id)

    async def get_by_codigo(self, codigo_evento: str) -> EventoCultural | None:
        normalized = codigo_evento.strip()
        for item in self._items.values():
            if item.codigo_evento == normalized:
                return item
        return None

    async def list_all(self) -> list[EventoCultural]:
        return sorted(self._items.values(), key=lambda item: (item.data_inicio, item.nome))

    async def list_by_tipo(self, tipo: TipoEventoCultural) -> list[EventoCultural]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: (item.data_inicio, item.nome))

    async def list_by_municipio(self, municipio: str) -> list[EventoCultural]:
        normalized = municipio.strip().lower()
        values = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(values, key=lambda item: (item.data_inicio, item.nome))

    async def list_by_status(self, status: StatusEventoCultural) -> list[EventoCultural]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: (item.data_inicio, item.nome))

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[EventoCultural]:
        values = [
            item
            for item in self._items.values()
            if item.data_inicio >= data_inicio and item.data_fim <= data_fim
        ]
        return sorted(values, key=lambda item: (item.data_inicio, item.nome))

    async def delete(self, evento_id: UUID) -> bool:
        return self._items.pop(evento_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"EVT/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_evento.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryGrupoArtisticoRepository(GrupoArtisticoRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, GrupoArtistico] = {}

    async def save(self, grupo: GrupoArtistico) -> GrupoArtistico:
        self._items[grupo.id] = grupo
        return grupo

    async def get_by_id(self, grupo_id: UUID) -> GrupoArtistico | None:
        return self._items.get(grupo_id)

    async def get_by_codigo(self, codigo_grupo: str) -> GrupoArtistico | None:
        normalized = codigo_grupo.strip()
        for item in self._items.values():
            if item.codigo_grupo == normalized:
                return item
        return None

    async def list_all(self) -> list[GrupoArtistico]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_tipo(self, tipo: TipoGrupoArtistico) -> list[GrupoArtistico]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_municipio(self, municipio: str) -> list[GrupoArtistico]:
        normalized = municipio.strip().lower()
        values = [
            item for item in self._items.values() if (item.municipio or "").lower() == normalized
        ]
        return sorted(values, key=lambda item: item.nome)

    async def delete(self, grupo_id: UUID) -> bool:
        return self._items.pop(grupo_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"GRP/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_grupo.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryPatrimonioImaterialRepository(PatrimonioImaterialRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, PatrimonioImaterial] = {}

    async def save(self, patrimonio: PatrimonioImaterial) -> PatrimonioImaterial:
        self._items[patrimonio.id] = patrimonio
        return patrimonio

    async def get_by_id(self, patrimonio_id: UUID) -> PatrimonioImaterial | None:
        return self._items.get(patrimonio_id)

    async def get_by_registro(self, registro_pni: str) -> PatrimonioImaterial | None:
        normalized = registro_pni.strip()
        for item in self._items.values():
            if item.registro_pni == normalized:
                return item
        return None

    async def list_all(self) -> list[PatrimonioImaterial]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_categoria(
        self, categoria: CategoriaPatrimonioImaterial
    ) -> list[PatrimonioImaterial]:
        values = [item for item in self._items.values() if item.categoria == categoria]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_municipio(self, municipio: str) -> list[PatrimonioImaterial]:
        normalized = municipio.strip().lower()
        values = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_status(self, status: StatusPatrimonioImaterial) -> list[PatrimonioImaterial]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: item.nome)

    async def delete(self, patrimonio_id: UUID) -> bool:
        return self._items.pop(patrimonio_id, None) is not None

    async def next_registro(self) -> str:
        year = date.today().year
        prefix = f"PIM/{year}/"
        count = sum(1 for item in self._items.values() if item.registro_pni.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryEspacoCulturalRepository(EspacoCulturalRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, EspacoCultural] = {}

    async def save(self, espaco: EspacoCultural) -> EspacoCultural:
        self._items[espaco.id] = espaco
        return espaco

    async def get_by_id(self, espaco_id: UUID) -> EspacoCultural | None:
        return self._items.get(espaco_id)

    async def get_by_codigo(self, codigo_espaco: str) -> EspacoCultural | None:
        normalized = codigo_espaco.strip()
        for item in self._items.values():
            if item.codigo_espaco == normalized:
                return item
        return None

    async def list_all(self) -> list[EspacoCultural]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_tipo(self, tipo: TipoEspacoCultural) -> list[EspacoCultural]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_municipio(self, municipio: str) -> list[EspacoCultural]:
        normalized = municipio.strip().lower()
        values = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(values, key=lambda item: item.nome)

    async def delete(self, espaco_id: UUID) -> bool:
        return self._items.pop(espaco_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"ESP/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_espaco.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryProjetoCulturalRepository(ProjetoCulturalRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, ProjetoCultural] = {}

    async def save(self, projeto: ProjetoCultural) -> ProjetoCultural:
        self._items[projeto.id] = projeto
        return projeto

    async def get_by_id(self, projeto_id: UUID) -> ProjetoCultural | None:
        return self._items.get(projeto_id)

    async def get_by_codigo(self, codigo_projeto: str) -> ProjetoCultural | None:
        normalized = codigo_projeto.strip()
        for item in self._items.values():
            if item.codigo_projeto == normalized:
                return item
        return None

    async def list_all(self) -> list[ProjetoCultural]:
        return sorted(self._items.values(), key=lambda item: item.data_submissao, reverse=True)

    async def list_by_tipo(self, tipo: TipoProjetoCultural) -> list[ProjetoCultural]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: item.data_submissao, reverse=True)

    async def list_by_status(self, status: StatusProjetoCultural) -> list[ProjetoCultural]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: item.data_submissao, reverse=True)

    async def list_by_periodo(self, data_inicio: date, data_fim: date) -> list[ProjetoCultural]:
        values = [
            item for item in self._items.values() if data_inicio <= item.data_submissao <= data_fim
        ]
        return sorted(values, key=lambda item: item.data_submissao, reverse=True)

    async def delete(self, projeto_id: UUID) -> bool:
        return self._items.pop(projeto_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f"PROJ/{year}/"
        count = sum(1 for item in self._items.values() if item.codigo_projeto.startswith(prefix))
        return f"{prefix}{count + 1:05d}"


class InMemoryEditalRepository(EditalRepositoryPort):
    def __init__(self) -> None:
        self._items: dict[UUID, Edital] = {}

    async def save(self, edital: Edital) -> Edital:
        self._items[edital.id] = edital
        return edital

    async def get_by_id(self, edital_id: UUID) -> Edital | None:
        return self._items.get(edital_id)

    async def get_by_numero(self, numero: str) -> Edital | None:
        normalized = numero.strip()
        for item in self._items.values():
            if item.numero == normalized:
                return item
        return None

    async def list_all(self) -> list[Edital]:
        return sorted(self._items.values(), key=lambda item: item.data_publicacao, reverse=True)

    async def list_by_tipo(self, tipo: TipoEditalCultural) -> list[Edital]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: item.data_publicacao, reverse=True)

    async def list_by_fase(self, fase: FaseEditalCultural) -> list[Edital]:
        values = [item for item in self._items.values() if item.fase == fase]
        return sorted(values, key=lambda item: item.data_publicacao, reverse=True)

    async def list_by_periodo(self, data_inicio: datetime, data_fim: datetime) -> list[Edital]:
        values = [
            item for item in self._items.values() if data_inicio <= item.data_publicacao <= data_fim
        ]
        return sorted(values, key=lambda item: item.data_publicacao, reverse=True)

    async def find_ativos(self) -> list[Edital]:
        values = [item for item in self._items.values() if item.ativo]
        return sorted(values, key=lambda item: item.data_publicacao, reverse=True)

    async def delete(self, edital_id: UUID) -> bool:
        return self._items.pop(edital_id, None) is not None


class FakeCitizenService:
    def __init__(self, *, active: bool = True) -> None:
        self.active = active

    async def is_citizen_active(self, citizen_id: UUID) -> bool:
        return self.active


class FakeTurismoService(TurismoServicePort):
    def __init__(self, *, exists: bool = True) -> None:
        self.exists = exists

    async def atracao_exists(self, atracao_id: UUID) -> bool:
        return self.exists


class FakeEducacaoService(EducacaoServicePort):
    def __init__(self, *, exists: bool = True) -> None:
        self.exists = exists

    async def instituicao_exists(self, instituicao_id: UUID) -> bool:
        return self.exists


class FakeRequestService(RequestServicePort):
    async def create_request(
        self,
        *,
        request_type: str,
        entity_id: UUID,
        metadata: dict | None = None,
        citizen_id: UUID | None = None,
        numero_processo: str | None = None,
    ):
        return None
