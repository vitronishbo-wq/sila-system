from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.logistics.application.ports import GeosampaServicePort, LinhaRepositoryPort, ObrasPublicasServicePort, UrbanismoServicePort, VeiculoRepositoryPort, WorkflowServicePort
from app.modules.logistics.domain.enums import ModalTransporte, StatusLinha, StatusVeiculoOperacional, TipoVeiculo, TipoViagem
from app.modules.logistics.domain.models import Linha, Veiculo
from app.modules.logistics.core.exceptions import LinhaAlreadyExistsError, LinhaNotFoundError, VeiculoAlreadyExistsError, VeiculoNotFoundError

class LinhaService:

    def __init__(self, *, linha_repo: LinhaRepositoryPort, veiculo_repo: VeiculoRepositoryPort, geosampa_adapter: GeosampaServicePort | None=None, urbanismo_adapter: UrbanismoServicePort | None=None, obras_publicas_adapter: ObrasPublicasServicePort | None=None, workflow_adapter: WorkflowServicePort | None=None) -> None:
        self._linha_repo = linha_repo
        self._veiculo_repo = veiculo_repo
        self._geosampa_adapter = geosampa_adapter
        self._urbanismo_adapter = urbanismo_adapter
        self._obras_publicas_adapter = obras_publicas_adapter
        self._workflow_adapter = workflow_adapter

    def has_geosampa_adapter(self) -> bool:
        return self._geosampa_adapter is not None

    def has_urbanismo_adapter(self) -> bool:
        return self._urbanismo_adapter is not None

    def has_workflow_adapter(self) -> bool:
        return self._workflow_adapter is not None

    async def criar_linha(self, *, nome: str, modal: ModalTransporte, tipo_viagem: TipoViagem, origem: str, destino: str, itinerario: list[dict], extensao_km: Decimal, tempo_estimado_minutos: int, dias_operacao: list[str], horario_inicio: str, horario_fim: str, tarifa_base: Decimal, operadora_id: UUID, codigo: str | None=None, frequencia_media_minutos: int | None=None, codigo_corredor: str | None=None, observacoes: str | None=None) -> Linha:
        if self._geosampa_adapter:
            valida = await self._geosampa_adapter.rota_valida(itinerario=itinerario)
            if not valida:
                raise ValueError('Itinerario invalido para georreferenciamento')
        if self._urbanismo_adapter:
            zona_valida = await self._urbanismo_adapter.validar_zoneamento_rota(origem=origem, destino=destino)
            if not zona_valida:
                raise ValueError('Rota nao validada por urbanismo')
        if codigo_corredor and self._obras_publicas_adapter:
            corredor_valido = await self._obras_publicas_adapter.validar_corredor(codigo_corredor=codigo_corredor)
            if not corredor_valido:
                raise ValueError('Corredor viario invalido para criacao da linha')
        codigo_linha = codigo or await self._linha_repo.next_codigo()
        if await self._linha_repo.get_by_codigo(codigo_linha):
            raise LinhaAlreadyExistsError('Ja existe linha com este codigo')
        linha = Linha.criar(codigo=codigo_linha, nome=nome, modal=modal, tipo_viagem=tipo_viagem, origem=origem, destino=destino, itinerario=itinerario, extensao_km=extensao_km, tempo_estimado_minutos=tempo_estimado_minutos, dias_operacao=dias_operacao, horario_inicio=horario_inicio, horario_fim=horario_fim, tarifa_base=tarifa_base, operadora_id=operadora_id, frequencia_media_minutos=frequencia_media_minutos, observacoes=observacoes)
        linha.registrar_evento_auditoria(evento='linha_criada', payload={'codigo_corredor': codigo_corredor})
        saved = await self._linha_repo.save(linha)
        if self._workflow_adapter:
            workflow_id = await self._workflow_adapter.iniciar_fluxo(entidade='transportes_logistica_linha', referencia_id=saved.id, contexto={'codigo_linha': saved.codigo})
            saved.registrar_evento_auditoria(evento='workflow_iniciado', payload={'workflow_id': workflow_id})
            saved = await self._linha_repo.save(saved)
        return saved

    async def cadastrar_veiculo(self, *, placa: str, tipo: TipoVeiculo, marca: str, modelo: str, ano_fabricacao: int, ano_modelo: int, proprietario_id: UUID, proprietario_tipo: str, data_aquisicao: date, capacidade_passageiros: int | None=None, operadora_id: UUID | None=None, observacoes: str | None=None) -> Veiculo:
        if await self._veiculo_repo.get_by_placa(placa):
            raise VeiculoAlreadyExistsError('Ja existe veiculo com esta placa')
        veiculo = Veiculo.cadastrar(placa=placa, tipo=tipo, marca=marca, modelo=modelo, ano_fabricacao=ano_fabricacao, ano_modelo=ano_modelo, proprietario_id=proprietario_id, proprietario_tipo=proprietario_tipo, data_aquisicao=data_aquisicao, capacidade_passageiros=capacidade_passageiros, operadora_id=operadora_id, observacoes=observacoes)
        return await self._veiculo_repo.save(veiculo)

    async def vincular_veiculo(self, codigo_linha: str, *, placa: str) -> Linha:
        linha = await self._linha_repo.get_by_codigo(codigo_linha)
        if not linha:
            raise LinhaNotFoundError('Linha nao encontrada')
        veiculo = await self._veiculo_repo.get_by_placa(placa)
        if not veiculo:
            raise VeiculoNotFoundError('Veiculo nao encontrado')
        if veiculo.status != StatusVeiculoOperacional.ATIVO:
            raise ValueError('Veiculo nao esta ativo para vinculacao')
        linha.adicionar_veiculo(veiculo_id=veiculo.id, placa=veiculo.placa)
        linha.registrar_evento_auditoria(evento='veiculo_vinculado', payload={'veiculo_id': str(veiculo.id), 'placa': veiculo.placa})
        saved = await self._linha_repo.save(linha)
        await self._registrar_evento_workflow(workflow_id=saved.codigo, evento='linha_veiculo_vinculado', payload={'veiculo_id': str(veiculo.id)})
        return saved

    async def atualizar_tarifa(self, codigo_linha: str, *, valor: Decimal) -> Linha:
        linha = await self._linha_repo.get_by_codigo(codigo_linha)
        if not linha:
            raise LinhaNotFoundError('Linha nao encontrada')
        linha.atualizar_tarifa(valor)
        linha.registrar_evento_auditoria(evento='tarifa_atualizada', payload={'valor': str(linha.tarifa_base)})
        saved = await self._linha_repo.save(linha)
        await self._registrar_evento_workflow(workflow_id=saved.codigo, evento='linha_tarifa_atualizada', payload={'valor': str(saved.tarifa_base)})
        return saved

    async def registrar_indicadores(self, codigo_linha: str, *, demanda_media_diaria: int | None, ocupacao_media: Decimal | None, regularidade: Decimal | None, pontualidade: Decimal | None) -> Linha:
        linha = await self._linha_repo.get_by_codigo(codigo_linha)
        if not linha:
            raise LinhaNotFoundError('Linha nao encontrada')
        linha.registrar_indicadores_operacionais(demanda_media_diaria=demanda_media_diaria, ocupacao_media=ocupacao_media, regularidade=regularidade, pontualidade=pontualidade)
        linha.registrar_evento_auditoria(evento='indicadores_operacionais_atualizados')
        saved = await self._linha_repo.save(linha)
        await self._registrar_evento_workflow(workflow_id=saved.codigo, evento='linha_indicadores_atualizados', payload={'demanda_media_diaria': demanda_media_diaria, 'ocupacao_media': str(ocupacao_media) if ocupacao_media is not None else None, 'regularidade': str(regularidade) if regularidade is not None else None, 'pontualidade': str(pontualidade) if pontualidade is not None else None})
        return saved

    async def obter_linha(self, codigo_linha: str) -> Linha:
        linha = await self._linha_repo.get_by_codigo(codigo_linha)
        if not linha:
            raise LinhaNotFoundError('Linha nao encontrada')
        return linha

    async def listar_linhas(self, *, status: StatusLinha | None=None, modal: ModalTransporte | None=None, operadora_id: UUID | None=None, origem: str | None=None, destino: str | None=None) -> list[Linha]:
        return await self._linha_repo.list(status=status, modal=modal, operadora_id=operadora_id, origem=origem, destino=destino)

    async def obter_veiculo(self, placa: str) -> Veiculo:
        veiculo = await self._veiculo_repo.get_by_placa(placa)
        if not veiculo:
            raise VeiculoNotFoundError('Veiculo nao encontrado')
        return veiculo

    async def listar_veiculos(self, *, status: StatusVeiculoOperacional | None=None, tipo: TipoVeiculo | None=None, operadora_id: UUID | None=None) -> list[Veiculo]:
        return await self._veiculo_repo.list(status=status, tipo=tipo, operadora_id=operadora_id)

    async def _registrar_evento_workflow(self, *, workflow_id: str, evento: str, payload: dict) -> None:
        if not self._workflow_adapter:
            return
        await self._workflow_adapter.registrar_evento(workflow_id=workflow_id, evento=evento, payload=payload)
