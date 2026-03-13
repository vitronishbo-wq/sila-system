from __future__ import annotations
import asyncio
from datetime import date, datetime, timedelta
from uuid import uuid4
import pytest
from apps.backend.app.modules.public_security.application.services.mandado_service import MandadoService
from apps.backend.app.modules.public_security.application.services.ocorrencia_service import OcorrenciaService
from apps.backend.app.modules.public_security.application.services.policial_service import PolicialService
from apps.backend.app.modules.public_security.application.services.unidade_policial_service import UnidadePolicialService
from apps.backend.app.modules.public_security.domain.enums import PrioridadeOcorrencia, StatusMandado, TipoAgente, TipoMandado, TipoOcorrencia, TipoUnidadePolicial, TipoVinculo
from apps.backend.app.modules.public_security.tests._fakes import InMemoryMandadoRepository, InMemoryOcorrenciaRepository, InMemoryPolicialRepository, InMemoryUnidadePolicialRepository

def test_expedir_mandado_sucesso() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        mandado_repo = InMemoryMandadoRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        mandado_service = MandadoService(mandado_repo=mandado_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Delegacia Sul', tipo=TipoUnidadePolicial.DELEGACIA, municipio='Luanda', provincia='Luanda', endereco='Rua Sul', comandante='Delegado Sul')
        policial = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Manuel Dias', data_nascimento=date.today() - timedelta(days=365 * 34), cpf='123.123.123-99', rg='RG123999', tipo=TipoAgente.DELEGADO, vinculo=TipoVinculo.EFETIVO)
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, policial_responsavel_id=policial.id, tipo=TipoOcorrencia.ROUBO, prioridade=PrioridadeOcorrencia.ALTA, data_ocorrencia=datetime.now() - timedelta(hours=3), descricao='Roubo qualificado em estabelecimento', municipio='Luanda', provincia='Luanda')
        mandado = await mandado_service.expedir_mandado(ocorrencia_id=ocorrencia.id, tipo=TipoMandado.BUSCA_APREENSAO, autoridade_judicial='Juizo Criminal Central', data_expedicao=date.today(), data_validade=date.today() + timedelta(days=15), unidade_id=unidade.id, policial_responsavel_id=policial.id)
        assert mandado.numero_mandado.startswith('MD/')
        assert mandado.status == StatusMandado.EXPEDIDO
    asyncio.run(scenario())

def test_expedir_mandado_falha_ocorrencia_inexistente() -> None:

    async def scenario() -> None:
        service = MandadoService(mandado_repo=InMemoryMandadoRepository(), ocorrencia_repo=InMemoryOcorrenciaRepository(), policial_repo=InMemoryPolicialRepository())
        with pytest.raises(ValueError, match='Ocorrencia nao encontrada'):
            await service.expedir_mandado(ocorrencia_id=uuid4(), tipo=TipoMandado.PRISAO, autoridade_judicial='Juizo A', data_expedicao=date.today(), data_validade=date.today() + timedelta(days=10))
    asyncio.run(scenario())

def test_atualizar_status_mandado() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        mandado_repo = InMemoryMandadoRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        mandado_service = MandadoService(mandado_repo=mandado_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Delegacia Norte', tipo=TipoUnidadePolicial.DELEGACIA, municipio='Luanda', provincia='Luanda', endereco='Rua Norte', comandante='Delegado Norte')
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, tipo=TipoOcorrencia.FURTO, prioridade=PrioridadeOcorrencia.MEDIA, data_ocorrencia=datetime.now() - timedelta(hours=5), descricao='Furto de carga em armazem', municipio='Luanda', provincia='Luanda')
        mandado = await mandado_service.expedir_mandado(ocorrencia_id=ocorrencia.id, tipo=TipoMandado.PRISAO, autoridade_judicial='Juizo Provincial', data_expedicao=date.today(), data_validade=date.today() + timedelta(days=20))
        atualizado = await mandado_service.atualizar_status(mandado_id=mandado.id, status=StatusMandado.CUMPRIDO, observacoes='Cumprido sem resistencia')
        assert atualizado.status == StatusMandado.CUMPRIDO
        assert atualizado.ativo is True
    asyncio.run(scenario())