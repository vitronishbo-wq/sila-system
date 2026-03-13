from __future__ import annotations
import asyncio
from datetime import date
from uuid import uuid4
import pytest
from app.modules.infrastructure_sector.telecomunicacoes.application.services.espectro_service import EspectroService
from app.modules.infrastructure_sector.telecomunicacoes.application.services.operadora_service import OperadoraService
from app.modules.infrastructure_sector.telecomunicacoes.application.services.outorga_espectro_service import OutorgaEspectroService
from app.modules.infrastructure_sector.telecomunicacoes.domain.enums import StatusEspectro, TipoEspectro, TipoOperadora, TipoOutorga, TipoServico
from app.modules.infrastructure_sector.telecomunicacoes.tests._fakes import InMemoryEspectroRepository, InMemoryOperadoraRepository, InMemoryOutorgaEspectroRepository

def test_registrar_espectro_sucesso() -> None:

    async def scenario() -> None:
        service = EspectroService(espectro_repo=InMemoryEspectroRepository(), outorga_repo=InMemoryOutorgaEspectroRepository())
        espectro = await service.registrar_espectro(tipo=TipoEspectro.BANDA_LARGA, frequencia_inicial_mhz=700.0, frequencia_final_mhz=800.0, servico_principal=TipoServico.INTERNET_MOVEL, municipio='Luanda', provincia='Luanda')
        assert espectro.codigo_espectro.startswith('ESP/')
        assert espectro.status == StatusEspectro.DISPONIVEL
    asyncio.run(scenario())

def test_registrar_espectro_falha_outorga_inexistente() -> None:

    async def scenario() -> None:
        service = EspectroService(espectro_repo=InMemoryEspectroRepository(), outorga_repo=InMemoryOutorgaEspectroRepository())
        with pytest.raises(ValueError, match='Outorga'):
            await service.registrar_espectro(tipo=TipoEspectro.BANDA_ESTREITA, frequencia_inicial_mhz=430.0, frequencia_final_mhz=440.0, servico_principal=TipoServico.RADIO, municipio='Huambo', provincia='Huambo', outorga_id=uuid4())
    asyncio.run(scenario())

def test_vincular_outorga_em_espectro() -> None:

    async def scenario() -> None:
        operadora_repo = InMemoryOperadoraRepository()
        outorga_repo = InMemoryOutorgaEspectroRepository()
        espectro_repo = InMemoryEspectroRepository()
        operadora_service = OperadoraService(operadora_repo=operadora_repo)
        outorga_service = OutorgaEspectroService(outorga_repo=outorga_repo, operadora_repo=operadora_repo)
        espectro_service = EspectroService(espectro_repo=espectro_repo, outorga_repo=outorga_repo)
        operadora = await operadora_service.cadastrar_operadora(cnpj='88.888.888/0001-88', razao_social='Mobile Spectrum SA', tipo=TipoOperadora.AUTORIZATARIA, servicos_autorizados=[TipoServico.TELEFONIA_MOVEL], endereco='Rua Espectro', municipio='Luanda', provincia='Luanda', telefone='222888888', email='mobile@spectrum.ao', representante_legal='Nuno Banda', representante_documento='45645645677', representante_cargo='Diretor')
        outorga = await outorga_service.emitir_outorga(operadora_id=operadora.id, tipo_outorga=TipoOutorga.AUTORIZACAO, faixa_inicio_mhz=2500.0, faixa_fim_mhz=2600.0, data_outorga=date.today())
        espectro = await espectro_service.registrar_espectro(tipo=TipoEspectro.BANDA_LARGA, frequencia_inicial_mhz=2500.0, frequencia_final_mhz=2600.0, servico_principal=TipoServico.TELEFONIA_MOVEL, municipio='Luanda', provincia='Luanda')
        atualizado = await espectro_service.vincular_outorga(espectro_id=espectro.id, outorga_id=outorga.id)
        assert atualizado.outorga_id == outorga.id
        assert atualizado.status == StatusEspectro.OUTORGADO
    asyncio.run(scenario())