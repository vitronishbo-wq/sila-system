from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from app.modules.infrastructure_sector.telecomunicacoes.application.services.infraestrutura_service import InfraestruturaService
from app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusInfraestrutura, TipoInfraestrutura, TipoOperadora, TipoServico
from app.modules.infrastructure_sector.telecomunicacoes.tests._fakes import InMemoryInfraestruturaRepository, InMemoryOperadoraRepository

def test_cadastrar_infraestrutura_sucesso() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        infraestrutura_service = InfraestruturaService(infraestrutura_repo=InMemoryInfraestruturaRepository(), operadora_repo=operadora_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='55.555.555/0001-55', razao_social='Infra Telecom SA', tipo=TipoOperadora.PROVEDOR, servicos_autorizados=[TipoServico.INTERNET_FIXA], endereco='Av. Rede, 10', municipio='Luanda', provincia='Luanda', telefone='222555555', email='infra@telecom.ao', representante_legal='Ana Infra', representante_documento='55566677788', representante_cargo='Diretora')
        infraestrutura = await infraestrutura_service.cadastrar_infraestrutura(operadora_id=operadora.id, tipo=TipoInfraestrutura.FIBRA_OPTICA, identificador='FIB-LDA-001', municipio='Luanda', provincia='Luanda', data_implantacao=date.today())
        assert infraestrutura.codigo_infra.startswith('INF/')
        assert infraestrutura.status == StatusInfraestrutura.PLANEADA
    asyncio.run(scenario())

def test_cadastrar_infraestrutura_falha_sem_operadora() -> None:

    async def scenario() -> None:
        service = InfraestruturaService(infraestrutura_repo=InMemoryInfraestruturaRepository(), operadora_repo=InMemoryOperadoraRepository())
        with pytest.raises(ValueError, match='Operadora'):
            await service.cadastrar_infraestrutura(operadora_id=uuid4(), tipo=TipoInfraestrutura.TORRE, identificador='TRR-001', municipio='Huambo', provincia='Huambo', data_implantacao=date.today())
    asyncio.run(scenario())

def test_atualizar_status_infraestrutura() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        infraestrutura_repo = InMemoryInfraestruturaRepository()
        infraestrutura_service = InfraestruturaService(infraestrutura_repo=infraestrutura_repo, operadora_repo=operadora_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='56.666.777/0001-99', razao_social='Torres Angola', tipo=TipoOperadora.AUTORIZATARIA, servicos_autorizados=[TipoServico.TELEFONIA_MOVEL], endereco='Rua Torre', municipio='Benguela', provincia='Benguela', telefone='222666777', email='torres@angola.ao', representante_legal='Luis Torre', representante_documento='11222333444', representante_cargo='Gestor')
        infraestrutura = await infraestrutura_service.cadastrar_infraestrutura(operadora_id=operadora.id, tipo=TipoInfraestrutura.TORRE, identificador='TRR-BGU-010', municipio='Benguela', provincia='Benguela', data_implantacao=date.today())
        atualizada = await infraestrutura_service.atualizar_status(infraestrutura_id=infraestrutura.id, status=StatusInfraestrutura.ATIVA)
        assert atualizada.status == StatusInfraestrutura.ATIVA
        assert atualizada.ativo is True
    asyncio.run(scenario())