from __future__ import annotations
from datetime import date, datetime
from typing import Any
from uuid import UUID
from apps.backend.app.modules.civil_protection.application.ports.atendimento_repository_port import AtendimentoRepositoryPort
from apps.backend.app.modules.civil_protection.application.ports.bombeiro_repository_port import BombeiroRepositoryPort
from apps.backend.app.modules.civil_protection.application.ports.corporacao_repository_port import CorporacaoRepositoryPort
from apps.backend.app.modules.civil_protection.application.ports.despacho_repository_port import DespachoRepositoryPort
from apps.backend.app.modules.civil_protection.application.ports.ocorrencia_emergencial_repository_port import OcorrenciaEmergencialRepositoryPort
from apps.backend.app.modules.civil_protection.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.civil_protection.domain.enums import StatusAtendimento, StatusAgenteProtecao, StatusCorporacao, StatusDespacho, StatusOcorrenciaEmergencial, TipoOcorrenciaEmergencial
from apps.backend.app.modules.civil_protection.domain.models.atendimento import Atendimento
from apps.backend.app.modules.civil_protection.domain.models.bombeiro import Bombeiro
from apps.backend.app.modules.civil_protection.domain.models.corporacao import Corporacao
from apps.backend.app.modules.civil_protection.domain.models.despacho import Despacho
from apps.backend.app.modules.civil_protection.domain.models.ocorrencia_emergencial import OcorrenciaEmergencial

class InMemoryCorporacaoRepository(CorporacaoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Corporacao] = {}

    async def save(self, corporacao: Corporacao) -> Corporacao:
        self._items[corporacao.id] = corporacao
        return corporacao

    async def get_by_id(self, corporacao_id: UUID) -> Corporacao | None:
        return self._items.get(corporacao_id)

    async def get_by_codigo(self, codigo_corporacao: str) -> Corporacao | None:
        normalized = codigo_corporacao.strip()
        for item in self._items.values():
            if item.codigo_corporacao == normalized:
                return item
        return None

    async def list_all(self) -> list[Corporacao]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_municipio(self, municipio: str) -> list[Corporacao]:
        normalized = municipio.strip().lower()
        items = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(items, key=lambda item: item.nome)

    async def list_by_status(self, status: StatusCorporacao) -> list[Corporacao]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.nome)

    async def delete(self, corporacao_id: UUID) -> bool:
        return self._items.pop(corporacao_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'COR/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_corporacao.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryBombeiroRepository(BombeiroRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Bombeiro] = {}

    async def save(self, bombeiro: Bombeiro) -> Bombeiro:
        self._items[bombeiro.id] = bombeiro
        return bombeiro

    async def get_by_id(self, bombeiro_id: UUID) -> Bombeiro | None:
        return self._items.get(bombeiro_id)

    async def get_by_matricula(self, matricula: str) -> Bombeiro | None:
        normalized = matricula.strip()
        for item in self._items.values():
            if item.matricula == normalized:
                return item
        return None

    async def get_by_cpf(self, cpf: str) -> Bombeiro | None:
        normalized = cpf.strip()
        for item in self._items.values():
            if item.cpf == normalized:
                return item
        return None

    async def list_all(self) -> list[Bombeiro]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_corporacao(self, corporacao_id: UUID) -> list[Bombeiro]:
        items = [item for item in self._items.values() if item.corporacao_id == corporacao_id]
        return sorted(items, key=lambda item: item.nome)

    async def list_by_status(self, status: StatusAgenteProtecao) -> list[Bombeiro]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.nome)

    async def delete(self, bombeiro_id: UUID) -> bool:
        return self._items.pop(bombeiro_id, None) is not None

    async def next_matricula(self, corporacao_id: UUID) -> str:
        year = date.today().year
        fragment = str(corporacao_id).split('-')[0].upper()
        prefix = f'BOM/{fragment}/{year}/'
        count = sum((1 for item in self._items.values() if item.matricula.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryOcorrenciaEmergencialRepository(OcorrenciaEmergencialRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, OcorrenciaEmergencial] = {}

    async def save(self, ocorrencia: OcorrenciaEmergencial) -> OcorrenciaEmergencial:
        self._items[ocorrencia.id] = ocorrencia
        return ocorrencia

    async def get_by_id(self, ocorrencia_id: UUID) -> OcorrenciaEmergencial | None:
        return self._items.get(ocorrencia_id)

    async def get_by_codigo(self, codigo_ocorrencia: str) -> OcorrenciaEmergencial | None:
        normalized = codigo_ocorrencia.strip()
        for item in self._items.values():
            if item.codigo_ocorrencia == normalized:
                return item
        return None

    async def list_all(self) -> list[OcorrenciaEmergencial]:
        return sorted(self._items.values(), key=lambda item: item.data_ocorrencia, reverse=True)

    async def list_by_corporacao(self, corporacao_id: UUID) -> list[OcorrenciaEmergencial]:
        items = [item for item in self._items.values() if item.corporacao_id == corporacao_id]
        return sorted(items, key=lambda item: item.data_ocorrencia, reverse=True)

    async def list_by_tipo(self, tipo: TipoOcorrenciaEmergencial) -> list[OcorrenciaEmergencial]:
        items = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(items, key=lambda item: item.data_ocorrencia, reverse=True)

    async def list_by_status(self, status: StatusOcorrenciaEmergencial) -> list[OcorrenciaEmergencial]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.data_ocorrencia, reverse=True)

    async def list_by_periodo(self, inicio: datetime, fim: datetime) -> list[OcorrenciaEmergencial]:
        items = [item for item in self._items.values() if item.data_ocorrencia >= inicio and item.data_ocorrencia <= fim]
        return sorted(items, key=lambda item: item.data_ocorrencia, reverse=True)

    async def delete(self, ocorrencia_id: UUID) -> bool:
        return self._items.pop(ocorrencia_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'OCE/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_ocorrencia.startswith(prefix)))
        return f'{prefix}{count + 1:06d}'

class InMemoryDespachoRepository(DespachoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Despacho] = {}

    async def save(self, despacho: Despacho) -> Despacho:
        self._items[despacho.id] = despacho
        return despacho

    async def get_by_id(self, despacho_id: UUID) -> Despacho | None:
        return self._items.get(despacho_id)

    async def get_by_codigo(self, codigo_despacho: str) -> Despacho | None:
        normalized = codigo_despacho.strip()
        for item in self._items.values():
            if item.codigo_despacho == normalized:
                return item
        return None

    async def list_all(self) -> list[Despacho]:
        return sorted(self._items.values(), key=lambda item: item.data_despacho, reverse=True)

    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Despacho]:
        items = [item for item in self._items.values() if item.ocorrencia_id == ocorrencia_id]
        return sorted(items, key=lambda item: item.data_despacho, reverse=True)

    async def list_by_status(self, status: StatusDespacho) -> list[Despacho]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.data_despacho, reverse=True)

    async def delete(self, despacho_id: UUID) -> bool:
        return self._items.pop(despacho_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'DSP/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_despacho.startswith(prefix)))
        return f'{prefix}{count + 1:06d}'

class InMemoryAtendimentoRepository(AtendimentoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Atendimento] = {}

    async def save(self, atendimento: Atendimento) -> Atendimento:
        self._items[atendimento.id] = atendimento
        return atendimento

    async def get_by_id(self, atendimento_id: UUID) -> Atendimento | None:
        return self._items.get(atendimento_id)

    async def get_by_codigo(self, codigo_atendimento: str) -> Atendimento | None:
        normalized = codigo_atendimento.strip()
        for item in self._items.values():
            if item.codigo_atendimento == normalized:
                return item
        return None

    async def list_all(self) -> list[Atendimento]:
        return sorted(self._items.values(), key=lambda item: item.inicio_atendimento, reverse=True)

    async def list_by_ocorrencia(self, ocorrencia_id: UUID) -> list[Atendimento]:
        items = [item for item in self._items.values() if item.ocorrencia_id == ocorrencia_id]
        return sorted(items, key=lambda item: item.inicio_atendimento, reverse=True)

    async def list_by_despacho(self, despacho_id: UUID) -> list[Atendimento]:
        items = [item for item in self._items.values() if item.despacho_id == despacho_id]
        return sorted(items, key=lambda item: item.inicio_atendimento, reverse=True)

    async def list_by_status(self, status: StatusAtendimento) -> list[Atendimento]:
        items = [item for item in self._items.values() if item.status == status]
        return sorted(items, key=lambda item: item.inicio_atendimento, reverse=True)

    async def delete(self, atendimento_id: UUID) -> bool:
        return self._items.pop(atendimento_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'ATE/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_atendimento.startswith(prefix)))
        return f'{prefix}{count + 1:06d}'

class FakeRequestService(RequestServicePort):

    async def create_request(self, *, request_type: str, entity_id: UUID, metadata: dict[str, Any] | None=None, citizen_id: UUID | None=None, numero_processo: str | None=None) -> UUID | None:
        return None