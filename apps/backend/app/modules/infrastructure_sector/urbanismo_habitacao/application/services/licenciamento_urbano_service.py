from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.ambiente_service_port import AmbienteServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.financas_service_port import FinancasServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.licenca_urbanistica_repository_port import LicencaUrbanisticaRepositoryPort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.application.ports.workflow_service_port import WorkflowServicePort
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.enums import StatusLicencaUrbanistica, TipoAlvara
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.domain.models.licenca_urbanistica import LicencaUrbanistica
from apps.backend.app.modules.infrastructure_sector.urbanismo_habitacao.exceptions import LicencaUrbanisticaAlreadyExistsError, LicencaUrbanisticaNotFoundError

class LicenciamentoUrbanoService:

    def __init__(self, *, licenca_repo: LicencaUrbanisticaRepositoryPort, ambiente_adapter: AmbienteServicePort | None=None, request_service: RequestServicePort | None=None, workflow_adapter: WorkflowServicePort | None=None, financas_adapter: FinancasServicePort | None=None) -> None:
        self._licenca_repo = licenca_repo
        self._ambiente_adapter = ambiente_adapter
        self._request_service = request_service
        self._workflow_adapter = workflow_adapter
        self._financas_adapter = financas_adapter

    def has_ambiente_adapter(self) -> bool:
        return self._ambiente_adapter is not None

    def has_workflow_adapter(self) -> bool:
        return self._workflow_adapter is not None

    def has_financas_adapter(self) -> bool:
        return self._financas_adapter is not None

    async def criar(self, *, numero_processo: str, tipo_alvara: TipoAlvara, requerente_id: UUID, zoneamento_id: UUID, provincia: str, municipio: str | None=None, endereco_obra: str | None=None, area_construida_prevista: Decimal | None=None, codigo_licenca: str | None=None) -> LicencaUrbanistica:
        codigo = codigo_licenca or await self._licenca_repo.next_codigo()
        existente = await self._licenca_repo.get_by_codigo(codigo)
        if existente:
            raise LicencaUrbanisticaAlreadyExistsError('Ja existe licenca urbanistica com este codigo')
        item = LicencaUrbanistica.criar(codigo_licenca=codigo, numero_processo=numero_processo, tipo_alvara=tipo_alvara, requerente_id=requerente_id, zoneamento_id=zoneamento_id, provincia=provincia, municipio=municipio, endereco_obra=endereco_obra, area_construida_prevista=area_construida_prevista)
        saved = await self._licenca_repo.save(item)
        if self._request_service:
            req_id = await self._request_service.create({'tipo': 'licenciamento_urbanistico', 'referencia_id': str(saved.id), 'numero_processo': saved.numero_processo})
            saved.observacoes = f'request_id:{req_id}'
            saved = await self._licenca_repo.save(saved)
        if self._workflow_adapter:
            wf_id = await self._workflow_adapter.iniciar_fluxo(entidade='urbanismo_licenca', referencia_id=saved.id, contexto={'codigo_licenca': saved.codigo_licenca})
            sufixo = f'workflow_id:{wf_id}'
            saved.observacoes = f'{saved.observacoes}|{sufixo}' if saved.observacoes else sufixo
            saved = await self._licenca_repo.save(saved)
        return saved

    async def iniciar_analise(self, codigo_licenca: str) -> LicencaUrbanistica:
        item = await self._obter_ou_erro(codigo_licenca)
        item.iniciar_analise()
        return await self._licenca_repo.save(item)

    async def solicitar_pendencia(self, codigo_licenca: str, *, motivo: str) -> LicencaUrbanistica:
        item = await self._obter_ou_erro(codigo_licenca)
        item.solicitar_pendencia(motivo=motivo)
        return await self._licenca_repo.save(item)

    async def deferir(self, codigo_licenca: str, *, data_emissao: date, data_validade: date, tecnico_responsavel_id: UUID) -> LicencaUrbanistica:
        item = await self._obter_ou_erro(codigo_licenca)
        if self._ambiente_adapter:
            licenca_ok = await self._ambiente_adapter.validar_licenca_ambiental(item.zoneamento_id)
            if not licenca_ok:
                raise ValueError('Pendencia ambiental impede deferimento da licenca')
        item.deferir(data_emissao=data_emissao, data_validade=data_validade, tecnico_responsavel_id=tecnico_responsavel_id)
        saved = await self._licenca_repo.save(item)
        if self._financas_adapter:
            taxa = await self._financas_adapter.calcular_taxa_licenciamento(tipo_alvara=saved.tipo_alvara, area_construida_prevista=saved.area_construida_prevista)
            cobranca_id = await self._financas_adapter.registrar_cobranca(referencia_id=saved.id, descricao=f'Taxa licenciamento {saved.codigo_licenca}', valor=taxa)
            sufixo = f'cobranca_id:{cobranca_id}'
            saved.observacoes = f'{saved.observacoes}|{sufixo}' if saved.observacoes else sufixo
            saved = await self._licenca_repo.save(saved)
        if self._workflow_adapter:
            await self._workflow_adapter.registrar_evento(workflow_id=saved.codigo_licenca, evento='licenca_deferida', payload={'status': saved.status.value})
        return saved

    async def indeferir(self, codigo_licenca: str, *, motivo: str) -> LicencaUrbanistica:
        item = await self._obter_ou_erro(codigo_licenca)
        item.indeferir(motivo=motivo)
        return await self._licenca_repo.save(item)

    async def cancelar(self, codigo_licenca: str, *, motivo: str) -> LicencaUrbanistica:
        item = await self._obter_ou_erro(codigo_licenca)
        item.cancelar(motivo=motivo)
        return await self._licenca_repo.save(item)

    async def obter_por_codigo(self, codigo_licenca: str) -> LicencaUrbanistica:
        return await self._obter_ou_erro(codigo_licenca)

    async def listar(self, *, status: StatusLicencaUrbanistica | None=None, tipo_alvara: TipoAlvara | None=None, provincia: str | None=None) -> list[LicencaUrbanistica]:
        return await self._licenca_repo.list(status=status, tipo_alvara=tipo_alvara, provincia=provincia)

    async def _obter_ou_erro(self, codigo_licenca: str) -> LicencaUrbanistica:
        item = await self._licenca_repo.get_by_codigo(codigo_licenca)
        if not item:
            raise LicencaUrbanisticaNotFoundError('Licenca urbanistica nao encontrada')
        return item