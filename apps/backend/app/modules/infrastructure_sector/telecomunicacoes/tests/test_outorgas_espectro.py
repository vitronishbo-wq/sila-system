from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from app.modules.infrastructure_sector.telecomunicacoes.application.services.outorga_espectro_service import OutorgaEspectroService
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusOutorga, TipoOperadora, TipoOutorga, TipoServico
from app.modules.infrastructure_sector.telecomunicacoes.tests._fakes import InMemoryOperadoraRepository, InMemoryOutorgaEspectroRepository

def test_emitir_outorga_sucesso() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        outorga_service = OutorgaEspectroService(outorga_repo=InMemoryOutorgaEspectroRepository(), operadora_repo=operadora_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='66.666.666/0001-66', razao_social='Radio Link SA', tipo=TipoOperadora.CONCESSIONARIA, servicos_autorizados=[TipoServico.COMUNICACAO_DADOS], endereco='Av. Sinal, 120', municipio='Luanda', provincia='Luanda', telefone='222666666', email='radio@link.ao', representante_legal='Marta Link', representante_documento='12312312399', representante_cargo='Administradora')
        outorga = await outorga_service.emitir_outorga(operadora_id=operadora.id, tipo_outorga=TipoOutorga.AUTORIZACAO, faixa_inicio_mhz=1800.0, faixa_fim_mhz=2100.0, data_outorga=date.today())
        assert outorga.numero_outorga.startswith('OUT/')
        assert outorga.status == StatusOutorga.EM_ANALISE
    asyncio.run(scenario())

def test_emitir_outorga_falha_sem_operadora() -> None:

    async def scenario() -> None:
        service = OutorgaEspectroService(outorga_repo=InMemoryOutorgaEspectroRepository(), operadora_repo=InMemoryOperadoraRepository())
        with pytest.raises(ValueError, match='Operadora'):
            await service.emitir_outorga(operadora_id=uuid4(), tipo_outorga=TipoOutorga.LICENCA, faixa_inicio_mhz=3500.0, faixa_fim_mhz=3700.0, data_outorga=date.today())
    asyncio.run(scenario())

def test_atualizar_status_outorga() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        outorga_repo = InMemoryOutorgaEspectroRepository()
        service = OutorgaEspectroService(outorga_repo=outorga_repo, operadora_repo=operadora_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='77.777.777/0001-77', razao_social='Banda 5G SA', tipo=TipoOperadora.AUTORIZATARIA, servicos_autorizados=[TipoServico.INTERNET_MOVEL], endereco='Rua 5G', municipio='Luanda', provincia='Luanda', telefone='222777777', email='5g@banda.ao', representante_legal='Pedro Banda', representante_documento='32132132188', representante_cargo='Diretor')
        outorga = await service.emitir_outorga(operadora_id=operadora.id, tipo_outorga=TipoOutorga.AUTORIZACAO, faixa_inicio_mhz=3400.0, faixa_fim_mhz=3600.0, data_outorga=date.today())
        atualizada = await service.atualizar_status(outorga_id=outorga.id, status=StatusOutorga.DEFERIDA)
        assert atualizada.status == StatusOutorga.DEFERIDA
        assert atualizada.ativo is True
    asyncio.run(scenario())