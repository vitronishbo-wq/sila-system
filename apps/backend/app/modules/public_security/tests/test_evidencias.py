from __future__ import annotations
import asyncio
from datetime import date, datetime, timedelta
from uuid import uuid4
import pytest
from apps.backend.app.modules.public_security.application.services.cadeia_custodia_service import CadeiaCustodiaService
from apps.backend.app.modules.public_security.application.services.evidencia_service import EvidenciaService
from apps.backend.app.modules.public_security.application.services.ocorrencia_service import OcorrenciaService
from apps.backend.app.modules.public_security.application.services.policial_service import PolicialService
from apps.backend.app.modules.public_security.application.services.prova_pericial_service import ProvaPericialService
from apps.backend.app.modules.public_security.application.services.unidade_policial_service import UnidadePolicialService
from apps.backend.app.modules.public_security.application.services.vestigio_service import VestigioService
from apps.backend.app.modules.public_security.domain.enums import PrioridadeOcorrencia, StatusEvidencia, TipoAgente, TipoEvidencia, TipoOcorrencia, TipoProva, TipoUnidadePolicial, TipoVestigio, TipoVinculo
from apps.backend.app.modules.public_security.tests._fakes import InMemoryCadeiaCustodiaRepository, InMemoryEvidenciaRepository, InMemoryOcorrenciaRepository, InMemoryPolicialRepository, InMemoryProvaPericialRepository, InMemoryUnidadePolicialRepository, InMemoryVestigioRepository

def test_registrar_evidencia_sucesso() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        cadeia_repo = InMemoryCadeiaCustodiaRepository()
        vestigio_repo = InMemoryVestigioRepository()
        evidencia_repo = InMemoryEvidenciaRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        prova_service = ProvaPericialService(prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        cadeia_service = CadeiaCustodiaService(cadeia_repo=cadeia_repo, prova_repo=prova_repo, policial_repo=policial_repo)
        vestigio_service = VestigioService(vestigio_repo=vestigio_repo, cadeia_repo=cadeia_repo, policial_repo=policial_repo)
        evidencia_service = EvidenciaService(evidencia_repo=evidencia_repo, vestigio_repo=vestigio_repo, cadeia_repo=cadeia_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Nucleo Evidencias', tipo=TipoUnidadePolicial.BASE_OPERACIONAL, municipio='Luanda', provincia='Luanda', endereco='Rua E1', comandante='Comandante E1')
        agente = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Analista Evidencias', data_nascimento=date.today() - timedelta(days=365 * 33), cpf='313.414.515-16', rg='RG313414', tipo=TipoAgente.PERITO, vinculo=TipoVinculo.EFETIVO)
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, policial_responsavel_id=agente.id, tipo=TipoOcorrencia.FALSIDADE, prioridade=PrioridadeOcorrencia.ALTA, data_ocorrencia=datetime.now() - timedelta(hours=3), descricao='Ocorrencia para registro de evidencia', municipio='Luanda', provincia='Luanda')
        prova = await prova_service.coletar_prova(ocorrencia_id=ocorrencia.id, tipo=TipoProva.DOCUMENTAL, descricao='Documentos para análise', local_coleta='Arquivo A', coletado_por_id=agente.id)
        cadeia = await cadeia_service.iniciar_cadeia(prova_id=prova.id, local_atual='Cofre E1', responsavel_id=agente.id)
        vestigio = await vestigio_service.registrar_vestigio(cadeia_custodia_id=cadeia.id, tipo=TipoVestigio.DOCUMENTO, descricao='Documento original coletado', localizacao='Prateleira 2', coletado_por_id=agente.id)
        evidencia = await evidencia_service.registrar_evidencia(vestigio_id=vestigio.id, tipo=TipoEvidencia.DOCUMENTAL, descricao='Evidencia documental autenticada', fonte='Arquivo central', confiabilidade=5, analisado_por_id=agente.id)
        assert evidencia.codigo_evidencia.startswith('EVD/')
        assert evidencia.status == StatusEvidencia.REGISTRADA
    asyncio.run(scenario())

def test_registrar_evidencia_falha_vestigio_inexistente() -> None:

    async def scenario() -> None:
        service = EvidenciaService(evidencia_repo=InMemoryEvidenciaRepository(), vestigio_repo=InMemoryVestigioRepository(), cadeia_repo=InMemoryCadeiaCustodiaRepository(), policial_repo=InMemoryPolicialRepository())
        with pytest.raises(ValueError, match='Vestigio nao encontrado'):
            await service.registrar_evidencia(vestigio_id=uuid4(), tipo=TipoEvidencia.FISICA, descricao='Evidencia sem vestigio base', fonte='Fonte X')
    asyncio.run(scenario())

def test_atualizar_status_evidencia() -> None:

    async def scenario() -> None:
        unidade_repo = InMemoryUnidadePolicialRepository()
        policial_repo = InMemoryPolicialRepository()
        ocorrencia_repo = InMemoryOcorrenciaRepository()
        prova_repo = InMemoryProvaPericialRepository()
        cadeia_repo = InMemoryCadeiaCustodiaRepository()
        vestigio_repo = InMemoryVestigioRepository()
        evidencia_repo = InMemoryEvidenciaRepository()
        unidade_service = UnidadePolicialService(unidade_repo=unidade_repo)
        policial_service = PolicialService(policial_repo=policial_repo, unidade_repo=unidade_repo)
        ocorrencia_service = OcorrenciaService(ocorrencia_repo=ocorrencia_repo, unidade_repo=unidade_repo, policial_repo=policial_repo)
        prova_service = ProvaPericialService(prova_repo=prova_repo, ocorrencia_repo=ocorrencia_repo, policial_repo=policial_repo)
        cadeia_service = CadeiaCustodiaService(cadeia_repo=cadeia_repo, prova_repo=prova_repo, policial_repo=policial_repo)
        vestigio_service = VestigioService(vestigio_repo=vestigio_repo, cadeia_repo=cadeia_repo, policial_repo=policial_repo)
        evidencia_service = EvidenciaService(evidencia_repo=evidencia_repo, vestigio_repo=vestigio_repo, cadeia_repo=cadeia_repo, policial_repo=policial_repo)
        unidade = await unidade_service.cadastrar_unidade(nome='Nucleo Evidencias B', tipo=TipoUnidadePolicial.BASE_OPERACIONAL, municipio='Bengo', provincia='Bengo', endereco='Rua E2', comandante='Comandante E2')
        agente = await policial_service.cadastrar_policial(unidade_id=unidade.id, nome='Analista B', data_nascimento=date.today() - timedelta(days=365 * 34), cpf='717.818.919-20', rg='RG717818', tipo=TipoAgente.PERITO, vinculo=TipoVinculo.EFETIVO)
        ocorrencia = await ocorrencia_service.registrar_ocorrencia(unidade_id=unidade.id, policial_responsavel_id=agente.id, tipo=TipoOcorrencia.DANO, prioridade=PrioridadeOcorrencia.MEDIA, data_ocorrencia=datetime.now() - timedelta(days=1), descricao='Ocorrencia para update de evidencia', municipio='Bengo', provincia='Bengo')
        prova = await prova_service.coletar_prova(ocorrencia_id=ocorrencia.id, tipo=TipoProva.DIGITAL, descricao='Arquivo digital para evidência', local_coleta='Sala B')
        cadeia = await cadeia_service.iniciar_cadeia(prova_id=prova.id, local_atual='Cofre E2', responsavel_id=agente.id)
        vestigio = await vestigio_service.registrar_vestigio(cadeia_custodia_id=cadeia.id, tipo=TipoVestigio.MIDIA_DIGITAL, descricao='HD externo apreendido', localizacao='Armario 5', coletado_por_id=agente.id)
        evidencia = await evidencia_service.registrar_evidencia(vestigio_id=vestigio.id, tipo=TipoEvidencia.DIGITAL, descricao='Evidencia digital indexada', fonte='Laboratorio digital', confiabilidade=4)
        atualizada = await evidencia_service.atualizar_status(evidencia_id=evidencia.id, status=StatusEvidencia.VALIDADA, observacoes='Validada em conferência técnica')
        assert atualizada.status == StatusEvidencia.VALIDADA
        assert atualizada.ativo is True
    asyncio.run(scenario())