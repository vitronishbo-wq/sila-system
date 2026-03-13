from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.logistics.application.ports import FinancasServicePort, FrotaRepositoryPort, SegurancaPublicaServicePort, ServiceRequestsServicePort, WorkflowServicePort
from app.modules.logistics.domain.enums import StatusFrota, TipoTarifa
from app.modules.logistics.domain.models import FiscalizacaoTransporte, Frota, Manutencao, Tarifa
from app.modules.logistics.core.exceptions import FrotaAlreadyExistsError, FrotaNotFoundError

class FrotaService:

    def __init__(self, *, frota_repo: FrotaRepositoryPort, workflow_adapter: WorkflowServicePort | None=None, service_requests_adapter: ServiceRequestsServicePort | None=None, financas_adapter: FinancasServicePort | None=None, seguranca_publica_adapter: SegurancaPublicaServicePort | None=None) -> None:
        self._frota_repo = frota_repo
        self._workflow_adapter = workflow_adapter
        self._service_requests_adapter = service_requests_adapter
        self._financas_adapter = financas_adapter
        self._seguranca_publica_adapter = seguranca_publica_adapter

    def has_workflow_adapter(self) -> bool:
        return self._workflow_adapter is not None

    def has_service_requests_adapter(self) -> bool:
        return self._service_requests_adapter is not None

    async def criar_frota(self, *, nome: str, operadora_id: UUID, municipio: str, provincia: str, codigo_frota: str | None=None, observacoes: str | None=None) -> Frota:
        codigo = codigo_frota or await self._frota_repo.next_codigo()
        if await self._frota_repo.get_by_codigo(codigo):
            raise FrotaAlreadyExistsError('Ja existe frota com este codigo')
        item = Frota.criar(codigo_frota=codigo, nome=nome, operadora_id=operadora_id, municipio=municipio, provincia=provincia, observacoes=observacoes)
        saved = await self._frota_repo.save(item)
        if self._service_requests_adapter:
            request_id = await self._service_requests_adapter.abrir_solicitacao({'tipo': 'frota_operacional', 'codigo_frota': saved.codigo_frota, 'municipio': saved.municipio, 'provincia': saved.provincia})
            sufixo = f'service_request_id:{request_id}'
            saved.observacoes = f'{saved.observacoes}|{sufixo}' if saved.observacoes else sufixo
            saved = await self._frota_repo.save(saved)
        if self._workflow_adapter:
            workflow_id = await self._workflow_adapter.iniciar_fluxo(entidade='transportes_logistica_frota', referencia_id=saved.id, contexto={'codigo_frota': saved.codigo_frota})
            saved.registrar_evento_auditoria(evento='frota_criada', payload={'workflow_id': workflow_id})
            saved = await self._frota_repo.save(saved)
        return saved

    async def adicionar_veiculo(self, codigo_frota: str, *, veiculo_id: UUID, placa: str, tipo: str, capacidade: int | None=None) -> Frota:
        item = await self._obter_ou_erro(codigo_frota)
        if self._seguranca_publica_adapter:
            regular = await self._seguranca_publica_adapter.validar_regularidade_veiculo(placa=placa)
            if not regular:
                raise ValueError('Veiculo irregular para vinculacao na frota')
        item.adicionar_veiculo(veiculo_id=veiculo_id, placa=placa, tipo=tipo, capacidade=capacidade)
        item.registrar_evento_auditoria(evento='veiculo_adicionado', payload={'veiculo_id': str(veiculo_id), 'placa': placa.upper()})
        saved = await self._frota_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='frota_veiculo_adicionado', payload={'veiculo_id': str(veiculo_id)})
        return saved

    async def registrar_manutencao(self, codigo_frota: str, *, veiculo_id: UUID, tipo: str, oficina: str, custo: Decimal, data_manutencao: date | None=None, observacoes: str | None=None) -> Frota:
        item = await self._obter_ou_erro(codigo_frota)
        manutencao = Manutencao.registrar(veiculo_id=veiculo_id, tipo=tipo, oficina=oficina, custo=custo, data_manutencao=data_manutencao, observacoes=observacoes)
        item.registrar_manutencao(manutencao)
        item.registrar_evento_auditoria(evento='manutencao_registrada', payload={'manutencao_id': str(manutencao.id), 'veiculo_id': str(veiculo_id)})
        if self._financas_adapter:
            registrado = await self._financas_adapter.registrar_despesa_manutencao(frota_id=item.id, veiculo_id=veiculo_id, valor=manutencao.custo, descricao=f'Manutencao {manutencao.tipo}')
            if not registrado:
                raise ValueError('Falha ao registrar despesa de manutencao em Financas')
        saved = await self._frota_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='frota_manutencao_registrada', payload={'manutencao_id': str(manutencao.id), 'custo': str(manutencao.custo)})
        return saved

    async def atualizar_tarifa(self, codigo_frota: str, *, tipo_tarifa: TipoTarifa, valor: Decimal, motivo: str, data_inicio_vigencia: date | None=None, data_fim_vigencia: date | None=None) -> Frota:
        item = await self._obter_ou_erro(codigo_frota)
        if self._financas_adapter:
            tarifa_valida = await self._financas_adapter.validar_tarifa(valor=valor, tipo=tipo_tarifa.value)
            if not tarifa_valida:
                raise ValueError('Tarifa invalida para politica financeira vigente')
        tarifa = Tarifa.definir(tipo=tipo_tarifa, valor=valor, data_inicio_vigencia=data_inicio_vigencia, data_fim_vigencia=data_fim_vigencia, motivo=motivo)
        item.atualizar_tarifa(tarifa)
        item.registrar_evento_auditoria(evento='tarifa_atualizada', payload={'tarifa_id': str(tarifa.id), 'tipo': tarifa.tipo.value, 'valor': str(tarifa.valor)})
        saved = await self._frota_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='frota_tarifa_atualizada', payload={'tarifa_id': str(tarifa.id), 'tipo': tarifa.tipo.value})
        return saved

    async def registrar_fiscalizacao(self, codigo_frota: str, *, fiscal_id: UUID, conformidade: bool, apontamentos: str, data_fiscalizacao: date | None=None, auto_infracao: str | None=None, observacoes: str | None=None) -> Frota:
        item = await self._obter_ou_erro(codigo_frota)
        fiscalizacao = FiscalizacaoTransporte.registrar(fiscal_id=fiscal_id, conformidade=conformidade, apontamentos=apontamentos, data_fiscalizacao=data_fiscalizacao, auto_infracao=auto_infracao, observacoes=observacoes)
        item.registrar_fiscalizacao(fiscalizacao)
        item.registrar_evento_auditoria(evento='fiscalizacao_registrada', payload={'fiscalizacao_id': str(fiscalizacao.id), 'conformidade': conformidade})
        saved = await self._frota_repo.save(item)
        await self._registrar_evento_workflow(saved, evento='frota_fiscalizacao_registrada', payload={'fiscalizacao_id': str(fiscalizacao.id), 'conformidade': conformidade})
        return saved

    async def obter_por_codigo(self, codigo_frota: str) -> Frota:
        return await self._obter_ou_erro(codigo_frota)

    async def listar(self, *, status: StatusFrota | None=None, operadora_id: UUID | None=None, municipio: str | None=None, provincia: str | None=None) -> list[Frota]:
        return await self._frota_repo.list(status=status, operadora_id=operadora_id, municipio=municipio, provincia=provincia)

    async def _obter_ou_erro(self, codigo_frota: str) -> Frota:
        item = await self._frota_repo.get_by_codigo(codigo_frota)
        if not item:
            raise FrotaNotFoundError('Frota nao encontrada')
        return item

    async def _registrar_evento_workflow(self, item: Frota, *, evento: str, payload: dict) -> None:
        if not self._workflow_adapter:
            return
        await self._workflow_adapter.registrar_evento(workflow_id=item.codigo_frota, evento=evento, payload=payload)
