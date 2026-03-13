from __future__ import annotations
import asyncio
from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4
import pytest
from app.modules.society.juventude.application.services.auxilio_service import AuxilioService
from app.modules.society.juventude.application.services.jovem_service import JovemService
from app.modules.society.juventude.domain.enums import Escolaridade, SituacaoOcupacional, StatusBeneficio, TipoAuxilio
from app.modules.society.juventude.tests._fakes import FakeCitizenService, FakeEducacaoService, FakeEmpregoService, InMemoryAuxilioRepository, InMemoryJovemRepository

def test_conceder_auxilio_sucesso() -> None:

    async def scenario() -> None:
        jovem_repo = InMemoryJovemRepository()
        jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        auxilio_service = AuxilioService(auxilio_repo=InMemoryAuxilioRepository(), jovem_repo=jovem_repo)
        jovem = await jovem_service.cadastrar_jovem(nome='Ana Jovem', data_nascimento=date.today() - timedelta(days=365 * 19), genero='F', naturalidade='Luanda', escolaridade=Escolaridade.MEDIO_COMPLETO, situacao_ocupacional=SituacaoOcupacional.ESTUDA, endereco='Rua D', municipio='Luanda', provincia='Luanda', citizen_id=uuid4())
        result = await auxilio_service.conceder_auxilio(jovem_id=jovem.id, tipo=TipoAuxilio.TRANSPORTE, data_inicio=date.today(), valor_mensal=Decimal('15000.00'))
        assert result.codigo_auxilio.startswith('AUX/')
        assert result.status == StatusBeneficio.ATIVO
    asyncio.run(scenario())

def test_conceder_auxilio_falha_jovem_inexistente() -> None:

    async def scenario() -> None:
        service = AuxilioService(auxilio_repo=InMemoryAuxilioRepository(), jovem_repo=InMemoryJovemRepository())
        with pytest.raises(ValueError, match='Jovem'):
            await service.conceder_auxilio(jovem_id=uuid4(), tipo=TipoAuxilio.ALIMENTACAO, data_inicio=date.today())
    asyncio.run(scenario())

def test_atualizar_status_auxilio() -> None:

    async def scenario() -> None:
        jovem_repo = InMemoryJovemRepository()
        jovem_service = JovemService(jovem_repo=jovem_repo, citizen_service=FakeCitizenService(active=True), educacao_service=FakeEducacaoService(matricula_ativa=True), emprego_service=FakeEmpregoService(candidatura_ativa=True))
        auxilio_repo = InMemoryAuxilioRepository()
        auxilio_service = AuxilioService(auxilio_repo=auxilio_repo, jovem_repo=jovem_repo)
        jovem = await jovem_service.cadastrar_jovem(nome='Pedro Jovem', data_nascimento=date.today() - timedelta(days=365 * 22), genero='M', naturalidade='Uige', escolaridade=Escolaridade.MEDIO_COMPLETO, situacao_ocupacional=SituacaoOcupacional.PROCURA_EMPREGO, endereco='Rua E', municipio='Uige', provincia='Uige', citizen_id=uuid4())
        auxilio = await auxilio_service.conceder_auxilio(jovem_id=jovem.id, tipo=TipoAuxilio.MORADIA, data_inicio=date.today())
        atualizado = await auxilio_service.atualizar_status(auxilio_id=auxilio.id, status=StatusBeneficio.SUSPENSO, observacoes='pendencia documental')
        assert atualizado.status == StatusBeneficio.SUSPENSO
    asyncio.run(scenario())