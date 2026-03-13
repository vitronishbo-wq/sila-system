from __future__ import annotations
import asyncio
from datetime import date, timedelta
import pytest
from apps.backend.app.modules.public_security.application.services.policial_service import PolicialService
from apps.backend.app.modules.public_security.application.services.unidade_policial_service import UnidadePolicialService
from apps.backend.app.modules.public_security.domain.enums import StatusAgente, TipoAgente, TipoUnidadePolicial, TipoVinculo
from apps.backend.app.modules.public_security.tests._fakes import InMemoryPolicialRepository, InMemoryUnidadePolicialRepository

def test_cadastrar_policial_sucesso() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='2a Delegacia', tipo=TipoUnidadePolicial.DELEGACIA, municipio='Luanda', provincia='Luanda', endereco='Rua 2', comandante='Delegado Chefe')
        policial = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Joao Silva', data_nascimento=date.today() - timedelta(days=365 * 30), cpf='123.456.789-00', rg='RG123456', tipo=TipoAgente.POLICIAL, vinculo=TipoVinculo.EFETIVO)
        assert policial.matricula.startswith('POL/')
        assert policial.status == StatusAgente.ATIVO
    asyncio.run(scenario())

def test_cadastrar_policial_falha_cpf_duplicado() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='3a Delegacia', tipo=TipoUnidadePolicial.DELEGACIA, municipio='Huambo', provincia='Huambo', endereco='Rua 3', comandante='Delegado H')
        payload = dict(unidade_id=unidade.id, nome='Ana Santos', data_nascimento=date.today() - timedelta(days=365 * 29), cpf='987.654.321-00', rg='RG998877', tipo=TipoAgente.POLICIAL, vinculo=TipoVinculo.EFETIVO)
        await policial_service.cadastrar_policial(**payload)
        with pytest.raises(ValueError, match='CPF'):
            await policial_service.cadastrar_policial(**payload)
    asyncio.run(scenario())

def test_ativar_porte_policial() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Companhia Sul', tipo=TipoUnidadePolicial.COMPANHIA, municipio='Benguela', provincia='Benguela', endereco='Av Sul', comandante='Major Sul')
        policial = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Carlos Costa', data_nascimento=date.today() - timedelta(days=365 * 33), cpf='321.654.987-10', rg='RG445566', tipo=TipoAgente.MILITAR, vinculo=TipoVinculo.EFETIVO)
        atualizado = await policial_service.ativar_porte(policial_id=policial.id, numero_porte='PA-2026-0001', data_validade=date.today() + timedelta(days=365))
        assert atualizado.porte_arma is True
        assert atualizado.numero_porte == 'PA-2026-0001'
    asyncio.run(scenario())