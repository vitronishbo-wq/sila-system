from __future__ import annotations
import asyncio
from uuid import uuid4
import pytest
from app.modules.society.cultura.application.services.patrimonio_imaterial_service import PatrimonioImaterialService
from app.modules.society.cultura.domain.enums import CategoriaPatrimonioImaterial, StatusPatrimonioImaterial
from app.modules.society.cultura.tests._fakes import FakeEducacaoService, FakeRequestService, FakeTurismoService, InMemoryPatrimonioImaterialRepository

def test_patrimonio_imaterial_registro_sucesso() -> None:

    async def scenario() -> None:
        service = PatrimonioImaterialService(patrimonio_repo=InMemoryPatrimonioImaterialRepository(), turismo_service=FakeTurismoService(exists=True), educacao_service=FakeEducacaoService(exists=True), request_service=FakeRequestService())
        patrimonio = await service.registrar_patrimonio(nome='Ritual da Kianda', categoria=CategoriaPatrimonioImaterial.RITUAL, descricao='Ritual ancestral de relacao com as aguas e memoria local.', comunidade='Ilha de Luanda', municipio='Luanda', provincia='Luanda', atracao_turistica_id=uuid4(), instituicao_educacional_id=uuid4())
        assert patrimonio.registro_pni.startswith('PIM/')
        assert patrimonio.status == StatusPatrimonioImaterial.PROPOSTO
    asyncio.run(scenario())

def test_patrimonio_imaterial_rejeita_atracao_inexistente() -> None:

    async def scenario() -> None:
        service = PatrimonioImaterialService(patrimonio_repo=InMemoryPatrimonioImaterialRepository(), turismo_service=FakeTurismoService(exists=False))
        with pytest.raises(ValueError, match='Atracao turistica'):
            await service.registrar_patrimonio(nome='Tradicao X', categoria=CategoriaPatrimonioImaterial.TRADICAO, descricao='Descricao valida e suficiente para registro formal.', comunidade='Comunidade X', municipio='Huambo', provincia='Huambo', atracao_turistica_id=uuid4())
    asyncio.run(scenario())

def test_patrimonio_imaterial_filtro_status() -> None:

    async def scenario() -> None:
        repo = InMemoryPatrimonioImaterialRepository()
        service = PatrimonioImaterialService(patrimonio_repo=repo)
        patrimonio = await service.registrar_patrimonio(nome='Lenda do Morro', categoria=CategoriaPatrimonioImaterial.EXPRESSAO_ORAL, descricao='Narrativa oral transmitida por varias geracoes na regiao.', comunidade='Bie', municipio='Kuito', provincia='Bie')
        await service.atualizar_patrimonio(patrimonio_id=patrimonio.id, status=StatusPatrimonioImaterial.REGISTRADO)
        registrados = await service.listar_patrimonios(status=StatusPatrimonioImaterial.REGISTRADO)
        assert len(registrados) == 1
        assert registrados[0].nome == 'Lenda do Morro'
    asyncio.run(scenario())