from __future__ import annotations
import asyncio
from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID, uuid4
from apps.backend.app.modules.society.juventude.application.ports.bolsa_estudo_repository_port import BolsaEstudoRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.estagio_juvenil_repository_port import EstagioJuvenilRepositoryPort
from apps.backend.app.modules.society.juventude.application.ports.inscricao_programa_repository_port import InscricaoProgramaRepositoryPort
from apps.backend.app.modules.society.juventude.application.services.bolsa_estudo_service import BolsaEstudoService
from apps.backend.app.modules.society.juventude.application.services.estagio_juvenil_service import EstagioJuvenilService
from apps.backend.app.modules.society.juventude.application.services.inscricao_programa_service import InscricaoProgramaService
from apps.backend.app.modules.society.juventude.application.services.jovem_service import JovemService
from apps.backend.app.modules.society.juventude.application.services.programa_service import ProgramaService
from apps.backend.app.modules.society.juventude.domain.enums import AreaInteresse, Escolaridade, SituacaoOcupacional, StatusEstagio, StatusInscricao, StatusPrograma, TipoBolsa, TipoPrograma
from apps.backend.app.modules.society.juventude.domain.models.bolsa_estudo import BolsaEstudo
from apps.backend.app.modules.society.juventude.domain.models.estagio_juvenil import EstagioJuvenil
from apps.backend.app.modules.society.juventude.domain.models.inscricao_programa import InscricaoPrograma
from apps.backend.app.modules.society.juventude.tests._fakes import FakeCitizenService, FakeEducacaoService, FakeEmpregoService, InMemoryJovemRepository, InMemoryProgramaRepository

class InMemoryBolsaRepository(BolsaEstudoRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, BolsaEstudo] = {}

    async def save(self, bolsa: BolsaEstudo) -> BolsaEstudo:
        self._items[bolsa.id] = bolsa
        return bolsa

    async def get_by_id(self, bolsa_id: UUID) -> BolsaEstudo | None:
        return self._items.get(bolsa_id)

    async def get_by_codigo(self, codigo_bolsa: str) -> BolsaEstudo | None:
        for item in self._items.values():
            if item.codigo_bolsa == codigo_bolsa:
                return item
        return None

    async def list_all(self) -> list[BolsaEstudo]:
        return list(self._items.values())

    async def list_by_jovem(self, jovem_id: UUID) -> list[BolsaEstudo]:
        return [i for i in self._items.values() if i.jovem_id == jovem_id]

    async def list_ativas(self) -> list[BolsaEstudo]:
        return [i for i in self._items.values() if i.ativa]

    async def delete(self, bolsa_id: UUID) -> bool:
        return self._items.pop(bolsa_id, None) is not None

    async def next_codigo(self) -> str:
        return f'BOL/{date.today().year}/{len(self._items) + 1:05d}'

class InMemoryEstagioRepository(EstagioJuvenilRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, EstagioJuvenil] = {}

    async def save(self, estagio: EstagioJuvenil) -> EstagioJuvenil:
        self._items[estagio.id] = estagio
        return estagio

    async def get_by_id(self, estagio_id: UUID) -> EstagioJuvenil | None:
        return self._items.get(estagio_id)

    async def get_by_codigo(self, codigo_estagio: str) -> EstagioJuvenil | None:
        for item in self._items.values():
            if item.codigo_estagio == codigo_estagio:
                return item
        return None

    async def list_all(self) -> list[EstagioJuvenil]:
        return list(self._items.values())

    async def list_by_jovem(self, jovem_id: UUID) -> list[EstagioJuvenil]:
        return [i for i in self._items.values() if i.jovem_id == jovem_id]

    async def list_by_status(self, status: StatusEstagio) -> list[EstagioJuvenil]:
        return [i for i in self._items.values() if i.status == status]

    async def delete(self, estagio_id: UUID) -> bool:
        return self._items.pop(estagio_id, None) is not None

    async def next_codigo(self) -> str:
        return f'EST/{date.today().year}/{len(self._items) + 1:05d}'

class InMemoryInscricaoRepository(InscricaoProgramaRepositoryPort):

    def __init__(self) -> None:
        self._items: dict[UUID, InscricaoPrograma] = {}

    async def save(self, inscricao: InscricaoPrograma) -> InscricaoPrograma:
        self._items[inscricao.id] = inscricao
        return inscricao

    async def get_by_id(self, inscricao_id: UUID) -> InscricaoPrograma | None:
        return self._items.get(inscricao_id)

    async def get_by_codigo(self, codigo_inscricao: str) -> InscricaoPrograma | None:
        for item in self._items.values():
            if item.codigo_inscricao == codigo_inscricao:
                return item
        return None

    async def list_all(self) -> list[InscricaoPrograma]:
        return list(self._items.values())

    async def list_by_jovem(self, jovem_id: UUID) -> list[InscricaoPrograma]:
        return [i for i in self._items.values() if i.jovem_id == jovem_id]

    async def list_by_programa(self, programa_id: UUID) -> list[InscricaoPrograma]:
        return [i for i in self._items.values() if i.programa_id == programa_id]

    async def list_by_status(self, status: StatusInscricao) -> list[InscricaoPrograma]:
        return [i for i in self._items.values() if i.status == status]

    async def exists_active_by_jovem_programa(self, jovem_id: UUID, programa_id: UUID) -> bool:
        return any((i.jovem_id == jovem_id and i.programa_id == programa_id and (i.status in {StatusInscricao.PENDENTE, StatusInscricao.CONFIRMADA}) for i in self._items.values()))

    async def count_confirmadas_by_programa(self, programa_id: UUID) -> int:
        return sum((1 for i in self._items.values() if i.programa_id == programa_id and i.status == StatusInscricao.CONFIRMADA))

    async def delete(self, inscricao_id: UUID) -> bool:
        return self._items.pop(inscricao_id, None) is not None

    async def next_codigo(self) -> str:
        return f'INS/{date.today().year}/{len(self._items) + 1:05d}'

def test_bolsa_estudo_fluxo_basico() -> None:

    async def scenario() -> None:
        jovem_repo = InMemoryJovemRepository()
        jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        jovem = await jovem_service.cadastrar_jovem(nome='Jovem Bolsa', data_nascimento=date.today() - timedelta(days=365 * 19), genero='F', naturalidade='Luanda', escolaridade=Escolaridade.MEDIO_COMPLETO, situacao_ocupacional=SituacaoOcupacional.ESTUDA, endereco='Rua A', municipio='Luanda', provincia='Luanda', citizen_id=uuid4())
        service = BolsaEstudoService(bolsa_repo=InMemoryBolsaRepository(), jovem_repo=jovem_repo)
        bolsa = await service.conceder_bolsa(jovem_id=jovem.id, tipo=TipoBolsa.PERMANENCIA, valor_mensal=Decimal('25000.00'), data_inicio=date.today())
        assert bolsa.codigo_bolsa.startswith('BOL/')
    asyncio.run(scenario())

def test_estagio_fluxo_basico() -> None:

    async def scenario() -> None:
        jovem_repo = InMemoryJovemRepository()
        jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        jovem = await jovem_service.cadastrar_jovem(nome='Jovem Estagio', data_nascimento=date.today() - timedelta(days=365 * 21), genero='M', naturalidade='Benguela', escolaridade=Escolaridade.SUPERIOR_INCOMPLETO, situacao_ocupacional=SituacaoOcupacional.ESTUDA_TRABALHA, endereco='Rua B', municipio='Benguela', provincia='Benguela', citizen_id=uuid4())
        service = EstagioJuvenilService(estagio_repo=InMemoryEstagioRepository(), jovem_repo=jovem_repo)
        estagio = await service.registrar_estagio(jovem_id=jovem.id, instituicao='Empresa Teste', area_interesse=AreaInteresse.TECNOLOGIA, cargo='Assistente', carga_horaria_semanal=20, data_inicio=date.today())
        updated = await service.atualizar_status(estagio_id=estagio.id, status=StatusEstagio.ATIVO)
        assert updated.status == StatusEstagio.ATIVO
    asyncio.run(scenario())

def test_inscricao_programa_valida_vagas_e_duplicidade() -> None:

    async def scenario() -> None:
        jovem_repo = InMemoryJovemRepository()
        programa_repo = InMemoryProgramaRepository()
        jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        programa_service = ProgramaService(programa_repo=programa_repo)
        jovem = await jovem_service.cadastrar_jovem(nome='Jovem Inscricao', data_nascimento=date.today() - timedelta(days=365 * 20), genero='M', naturalidade='Huambo', escolaridade=Escolaridade.MEDIO_COMPLETO, situacao_ocupacional=SituacaoOcupacional.PROCURA_EMPREGO, endereco='Rua C', municipio='Huambo', provincia='Huambo', citizen_id=uuid4())
        programa = await programa_service.criar_programa(nome='Programa Emprego Jovem', tipo=TipoPrograma.PRIMEIRO_EMPREGO, data_inicio=date.today(), vagas=5)
        programa.atualizar_status(StatusPrograma.INSCRICOES_ABERTAS)
        await programa_repo.save(programa)
        service = InscricaoProgramaService(inscricao_repo=InMemoryInscricaoRepository(), jovem_repo=jovem_repo, programa_repo=programa_repo)
        inscricao = await service.inscrever_jovem(programa_id=programa.id, jovem_id=jovem.id)
        assert inscricao.codigo_inscricao.startswith('INS/')
        try:
            await service.inscrever_jovem(programa_id=programa.id, jovem_id=jovem.id)
            assert False, 'Esperava erro de duplicidade'
        except ValueError:
            assert True
    asyncio.run(scenario())