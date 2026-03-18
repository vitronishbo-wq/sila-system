from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from apps.backend.app.modules.logistics.domain.ports import GeosampaServicePort, LinhaRepositoryPort, ObrasPublicasServicePort, UrbanismoServicePort, VeiculoRepositoryPort, WorkflowServicePort
from apps.backend.app.modules.logistics.domain.enums import ModalTransporte, StatusLinha, StatusVeiculoOperacional, TipoVeiculo, TipoViagem
from apps.backend.app.modules.logistics.domain.models import Linha, Veiculo
from apps.backend.app.modules.logistics.domain.services import LinhaDomainService

class LinhaService:

    def __init__(self, *, linha_repo: LinhaRepositoryPort, veiculo_repo: VeiculoRepositoryPort, geosampa_adapter: GeosampaServicePort | None=None, urbanismo_adapter: UrbanismoServicePort | None=None, obras_publicas_adapter: ObrasPublicasServicePort | None=None, workflow_adapter: WorkflowServicePort | None=None) -> None:
        self._domain = LinhaDomainService(linha_repo=linha_repo, veiculo_repo=veiculo_repo, geosampa_adapter=geosampa_adapter, urbanismo_adapter=urbanismo_adapter, obras_publicas_adapter=obras_publicas_adapter, workflow_adapter=workflow_adapter)

    def has_geosampa_adapter(self) -> bool:
        return self._domain.has_geosampa_adapter()

    def has_urbanismo_adapter(self) -> bool:
        return self._domain.has_urbanismo_adapter()

    def has_workflow_adapter(self) -> bool:
        return self._domain.has_workflow_adapter()

    async def criar_linha(self, *, nome: str, modal: ModalTransporte, tipo_viagem: TipoViagem, origem: str, destino: str, itinerario: list[dict], extensao_km: Decimal, tempo_estimado_minutos: int, dias_operacao: list[str], horario_inicio: str, horario_fim: str, tarifa_base: Decimal, operadora_id: UUID, codigo: str | None=None, frequencia_media_minutos: int | None=None, codigo_corredor: str | None=None, observacoes: str | None=None) -> Linha:
        return await self._domain.criar_linha(nome=nome, modal=modal, tipo_viagem=tipo_viagem, origem=origem, destino=destino, itinerario=itinerario, extensao_km=extensao_km, tempo_estimado_minutos=tempo_estimado_minutos, dias_operacao=dias_operacao, horario_inicio=horario_inicio, horario_fim=horario_fim, tarifa_base=tarifa_base, operadora_id=operadora_id, codigo=codigo, frequencia_media_minutos=frequencia_media_minutos, codigo_corredor=codigo_corredor, observacoes=observacoes)

    async def cadastrar_veiculo(self, *, placa: str, tipo: TipoVeiculo, marca: str, modelo: str, ano_fabricacao: int, ano_modelo: int, proprietario_id: UUID, proprietario_tipo: str, data_aquisicao: date, capacidade_passageiros: int | None=None, operadora_id: UUID | None=None, observacoes: str | None=None) -> Veiculo:
        return await self._domain.cadastrar_veiculo(placa=placa, tipo=tipo, marca=marca, modelo=modelo, ano_fabricacao=ano_fabricacao, ano_modelo=ano_modelo, proprietario_id=proprietario_id, proprietario_tipo=proprietario_tipo, data_aquisicao=data_aquisicao, capacidade_passageiros=capacidade_passageiros, operadora_id=operadora_id, observacoes=observacoes)

    async def vincular_veiculo(self, codigo_linha: str, *, placa: str) -> Linha:
        return await self._domain.vincular_veiculo(codigo_linha, placa=placa)

    async def atualizar_tarifa(self, codigo_linha: str, *, valor: Decimal) -> Linha:
        return await self._domain.atualizar_tarifa(codigo_linha, valor=valor)

    async def registrar_indicadores(self, codigo_linha: str, *, demanda_media_diaria: int | None, ocupacao_media: Decimal | None, regularidade: Decimal | None, pontualidade: Decimal | None) -> Linha:
        return await self._domain.registrar_indicadores(codigo_linha, demanda_media_diaria=demanda_media_diaria, ocupacao_media=ocupacao_media, regularidade=regularidade, pontualidade=pontualidade)

    async def obter_linha(self, codigo_linha: str) -> Linha:
        return await self._domain.obter_linha(codigo_linha)

    async def listar_linhas(self, *, status: StatusLinha | None=None, modal: ModalTransporte | None=None, operadora_id: UUID | None=None, origem: str | None=None, destino: str | None=None) -> list[Linha]:
        return await self._domain.listar_linhas(status=status, modal=modal, operadora_id=operadora_id, origem=origem, destino=destino)

    async def obter_veiculo(self, placa: str) -> Veiculo:
        return await self._domain.obter_veiculo(placa)

    async def listar_veiculos(self, *, status: StatusVeiculoOperacional | None=None, tipo: TipoVeiculo | None=None, operadora_id: UUID | None=None) -> list[Veiculo]:
        return await self._domain.listar_veiculos(status=status, tipo=tipo, operadora_id=operadora_id)