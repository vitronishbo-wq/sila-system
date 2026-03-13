from __future__ import annotations
from datetime import date
from uuid import UUID
from app.modules.society.juventude.application.ports.auxilio_repository_port import AuxilioRepositoryPort
from app.modules.society.juventude.application.ports.citizen_service_port import CitizenServicePort
from app.modules.society.juventude.application.ports.educacao_service_port import EducacaoServicePort
from app.modules.society.juventude.application.ports.emprego_service_port import EmpregoServicePort
from app.modules.society.juventude.application.ports.formacao_repository_port import FormacaoRepositoryPort
from app.modules.society.juventude.application.ports.jovem_repository_port import JovemRepositoryPort
from app.modules.society.juventude.application.ports.programa_repository_port import ProgramaRepositoryPort
from app.modules.society.juventude.application.ports.request_service_port import RequestServicePort
from app.modules.society.juventude.application.ports.risco_evasao_repository_port import RiscoEvasaoRepositoryPort
from app.modules.society.juventude.domain.enums import Escolaridade, FaixaEtaria, RiscoSocial, SituacaoOcupacional, StatusBeneficio, StatusFormacao, StatusPrograma, TipoAuxilio, TipoPrograma
from app.modules.society.juventude.domain.models.auxilio import Auxilio
from app.modules.society.juventude.domain.models.formacao_juvenil import FormacaoJuvenil
from app.modules.society.juventude.domain.models.jovem import Jovem
from app.modules.society.juventude.domain.models.programa_juvenil import ProgramaJuvenil
from app.modules.society.juventude.domain.models.risco_evasao import RiscoEvasao

class InMemoryJovemRepository(JovemRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Jovem] = {}

    async def save(self, jovem: Jovem) -> Jovem:
        self._items[jovem.id] = jovem
        return jovem

    async def get_by_id(self, jovem_id: UUID) -> Jovem | None:
        return self._items.get(jovem_id)

    async def get_by_registro(self, numero_registro: str) -> Jovem | None:
        normalized = numero_registro.strip()
        for item in self._items.values():
            if item.numero_registro == normalized:
                return item
        return None

    async def get_by_citizen(self, citizen_id: UUID) -> Jovem | None:
        for item in self._items.values():
            if item.citizen_id == citizen_id:
                return item
        return None

    async def list_all(self) -> list[Jovem]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_faixa_etaria(self, faixa_etaria: FaixaEtaria) -> list[Jovem]:
        values = [item for item in self._items.values() if item.faixa_etaria == faixa_etaria]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_escolaridade(self, escolaridade: Escolaridade) -> list[Jovem]:
        values = [item for item in self._items.values() if item.escolaridade == escolaridade]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_situacao(self, situacao: SituacaoOcupacional) -> list[Jovem]:
        values = [item for item in self._items.values() if item.situacao_ocupacional == situacao]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_municipio(self, municipio: str) -> list[Jovem]:
        normalized = municipio.strip().lower()
        values = [item for item in self._items.values() if item.municipio.lower() == normalized]
        return sorted(values, key=lambda item: item.nome)

    async def list_vulneraveis(self) -> list[Jovem]:
        values = [item for item in self._items.values() if item.vulnerabilidades]
        return sorted(values, key=lambda item: item.nome)

    async def delete(self, jovem_id: UUID) -> bool:
        return self._items.pop(jovem_id, None) is not None

    async def next_registro(self) -> str:
        year = date.today().year
        prefix = f'JOV/{year}/'
        count = sum((1 for item in self._items.values() if item.numero_registro.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryAuxilioRepository(AuxilioRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, Auxilio] = {}

    async def save(self, auxilio: Auxilio) -> Auxilio:
        self._items[auxilio.id] = auxilio
        return auxilio

    async def get_by_id(self, auxilio_id: UUID) -> Auxilio | None:
        return self._items.get(auxilio_id)

    async def get_by_codigo(self, codigo_auxilio: str) -> Auxilio | None:
        normalized = codigo_auxilio.strip()
        for item in self._items.values():
            if item.codigo_auxilio == normalized:
                return item
        return None

    async def list_all(self) -> list[Auxilio]:
        return sorted(self._items.values(), key=lambda item: item.codigo_auxilio)

    async def list_by_jovem(self, jovem_id: UUID) -> list[Auxilio]:
        values = [item for item in self._items.values() if item.jovem_id == jovem_id]
        return sorted(values, key=lambda item: item.codigo_auxilio)

    async def list_by_tipo(self, tipo: TipoAuxilio) -> list[Auxilio]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: item.codigo_auxilio)

    async def list_by_status(self, status: StatusBeneficio) -> list[Auxilio]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: item.codigo_auxilio)

    async def delete(self, auxilio_id: UUID) -> bool:
        return self._items.pop(auxilio_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'AUX/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_auxilio.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryProgramaRepository(ProgramaRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, ProgramaJuvenil] = {}

    async def save(self, programa: ProgramaJuvenil) -> ProgramaJuvenil:
        self._items[programa.id] = programa
        return programa

    async def get_by_id(self, programa_id: UUID) -> ProgramaJuvenil | None:
        return self._items.get(programa_id)

    async def get_by_codigo(self, codigo_programa: str) -> ProgramaJuvenil | None:
        normalized = codigo_programa.strip()
        for item in self._items.values():
            if item.codigo_programa == normalized:
                return item
        return None

    async def list_all(self) -> list[ProgramaJuvenil]:
        return sorted(self._items.values(), key=lambda item: item.nome)

    async def list_by_tipo(self, tipo: TipoPrograma) -> list[ProgramaJuvenil]:
        values = [item for item in self._items.values() if item.tipo == tipo]
        return sorted(values, key=lambda item: item.nome)

    async def list_by_status(self, status: StatusPrograma) -> list[ProgramaJuvenil]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: item.nome)

    async def delete(self, programa_id: UUID) -> bool:
        return self._items.pop(programa_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'PRG/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_programa.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryFormacaoRepository(FormacaoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, FormacaoJuvenil] = {}

    async def save(self, formacao: FormacaoJuvenil) -> FormacaoJuvenil:
        self._items[formacao.id] = formacao
        return formacao

    async def get_by_id(self, formacao_id: UUID) -> FormacaoJuvenil | None:
        return self._items.get(formacao_id)

    async def get_by_codigo(self, codigo_formacao: str) -> FormacaoJuvenil | None:
        normalized = codigo_formacao.strip()
        for item in self._items.values():
            if item.codigo_formacao == normalized:
                return item
        return None

    async def list_all(self) -> list[FormacaoJuvenil]:
        return sorted(self._items.values(), key=lambda item: item.codigo_formacao)

    async def list_by_jovem(self, jovem_id: UUID) -> list[FormacaoJuvenil]:
        values = [item for item in self._items.values() if item.jovem_id == jovem_id]
        return sorted(values, key=lambda item: item.codigo_formacao)

    async def list_by_programa(self, programa_id: UUID) -> list[FormacaoJuvenil]:
        values = [item for item in self._items.values() if item.programa_id == programa_id]
        return sorted(values, key=lambda item: item.codigo_formacao)

    async def list_by_status(self, status: StatusFormacao) -> list[FormacaoJuvenil]:
        values = [item for item in self._items.values() if item.status == status]
        return sorted(values, key=lambda item: item.codigo_formacao)

    async def delete(self, formacao_id: UUID) -> bool:
        return self._items.pop(formacao_id, None) is not None

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'FRM/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_formacao.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class InMemoryRiscoEvasaoRepository(RiscoEvasaoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, RiscoEvasao] = {}

    async def save(self, risco: RiscoEvasao) -> RiscoEvasao:
        self._items[risco.id] = risco
        return risco

    async def get_by_id(self, risco_id: UUID) -> RiscoEvasao | None:
        return self._items.get(risco_id)

    async def get_ativo_by_jovem(self, jovem_id: UUID) -> RiscoEvasao | None:
        values = [item for item in self._items.values() if item.jovem_id == jovem_id and item.ativo]
        if not values:
            return None
        values.sort(key=lambda item: item.data_avaliacao, reverse=True)
        return values[0]

    async def list_all(self) -> list[RiscoEvasao]:
        return sorted(self._items.values(), key=lambda item: item.data_avaliacao, reverse=True)

    async def list_by_nivel(self, nivel: RiscoSocial) -> list[RiscoEvasao]:
        values = [item for item in self._items.values() if item.nivel_risco == nivel]
        return sorted(values, key=lambda item: item.data_avaliacao, reverse=True)

    async def next_codigo(self) -> str:
        year = date.today().year
        prefix = f'RISK/{year}/'
        count = sum((1 for item in self._items.values() if item.codigo_risco.startswith(prefix)))
        return f'{prefix}{count + 1:05d}'

class FakeCitizenService(CitizenServicePort):

    def __init__(self, *, active: bool=True) -> None:
        self.active = active

    async def is_citizen_active(self, citizen_id: UUID) -> bool:
        return self.active

class FakeEducacaoService(EducacaoServicePort):

    def __init__(self, *, matricula_ativa: bool=True) -> None:
        self.matricula_ativa = matricula_ativa

    async def has_matricula_ativa(self, citizen_id: UUID) -> bool:
        return self.matricula_ativa

class FakeEmpregoService(EmpregoServicePort):

    def __init__(self, *, candidatura_ativa: bool=True) -> None:
        self.candidatura_ativa = candidatura_ativa

    async def has_candidatura_ativa(self, citizen_id: UUID) -> bool:
        return self.candidatura_ativa

class FakeRequestService(RequestServicePort):

    async def create_request(self, *, request_type: str, entity_id: UUID, metadata: dict | None=None, citizen_id: UUID | None=None, numero_processo: str | None=None):
        return None