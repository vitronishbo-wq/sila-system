from __future__ import annotations
from datetime import date
from apps.backend.app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from apps.backend.app.modules.resources.agricultura.domain.enums import StatusCadastroAmbiental, StatusZoneamento
from apps.backend.app.modules.resources.agricultura.domain.models.cadastro_ambiental import CadastroAmbiental
from apps.backend.app.modules.resources.agricultura.domain.models.zoneamento import Zoneamento
from apps.backend.app.modules.resources.agricultura.exceptions import CadastroAmbientalNotFoundError, ZoneamentoNotFoundError

class ZoneamentoService:

    def __init__(self, *, propriedade_service: PropriedadeService) -> None:
        self._propriedade_service = propriedade_service
        self._zoneamentos: dict[str, Zoneamento] = {}
        self._cadastros: dict[str, CadastroAmbiental] = {}
        self._seq_zoneamento = 0
        self._seq_cadastro = 0

    def _next_codigo_zoneamento(self) -> str:
        self._seq_zoneamento += 1
        return f'ZON/{date.today().year}/{self._seq_zoneamento:06d}'

    def _next_codigo_cadastro(self) -> str:
        self._seq_cadastro += 1
        return f'CAR/{date.today().year}/{self._seq_cadastro:06d}'

    async def registrar_zoneamento(self, *, codigo_propriedade: str, zona, aptidao_solo, area_zoneada_ha: float, culturas_recomendadas: list[str] | None=None, restricoes: list[str] | None=None, validade_ate: date | None=None, observacoes: str | None=None) -> Zoneamento:
        await self._propriedade_service.obter(codigo_propriedade)
        item = Zoneamento.registrar(codigo_propriedade=codigo_propriedade, zona=zona, aptidao_solo=aptidao_solo, area_zoneada_ha=area_zoneada_ha, culturas_recomendadas=culturas_recomendadas, restricoes=restricoes, validade_ate=validade_ate, observacoes=observacoes)
        item.codigo_zoneamento = self._next_codigo_zoneamento()
        self._zoneamentos[item.codigo_zoneamento] = item
        return item

    async def entrar_revisao(self, codigo_zoneamento: str) -> Zoneamento:
        item = self._zoneamentos.get(codigo_zoneamento)
        if not item:
            raise ZoneamentoNotFoundError('Zoneamento nao encontrado')
        item.entrar_revisao()
        return item

    async def revogar(self, codigo_zoneamento: str, *, motivo: str) -> Zoneamento:
        item = self._zoneamentos.get(codigo_zoneamento)
        if not item:
            raise ZoneamentoNotFoundError('Zoneamento nao encontrado')
        item.revogar(motivo)
        return item

    async def obter_zoneamento(self, codigo_zoneamento: str) -> Zoneamento:
        item = self._zoneamentos.get(codigo_zoneamento)
        if not item:
            raise ZoneamentoNotFoundError('Zoneamento nao encontrado')
        return item

    async def listar_zoneamentos(self, *, codigo_propriedade: str | None=None, status: StatusZoneamento | None=None) -> list[Zoneamento]:
        values = list(self._zoneamentos.values())
        if codigo_propriedade:
            values = [item for item in values if item.codigo_propriedade == codigo_propriedade]
        if status:
            values = [item for item in values if item.status == status]
        return values

    async def registrar_cadastro_ambiental(self, *, codigo_zoneamento: str, reserva_legal_percentual: float, app_percentual: float, area_protecao_ha: float, numero_processo: str | None=None) -> CadastroAmbiental:
        zoneamento = await self.obter_zoneamento(codigo_zoneamento)
        existente = next((item for item in self._cadastros.values() if item.codigo_zoneamento == codigo_zoneamento), None)
        if existente:
            raise ValueError('Ja existe cadastro ambiental para este zoneamento')
        cadastro = CadastroAmbiental.registrar(codigo_zoneamento=codigo_zoneamento, codigo_propriedade=zoneamento.codigo_propriedade, reserva_legal_percentual=reserva_legal_percentual, app_percentual=app_percentual, area_protecao_ha=area_protecao_ha, numero_processo=numero_processo)
        cadastro.codigo_cadastro_ambiental = self._next_codigo_cadastro()
        self._cadastros[cadastro.codigo_cadastro_ambiental] = cadastro
        return cadastro

    async def validar_cadastro(self, codigo_cadastro_ambiental: str, *, numero_processo: str) -> CadastroAmbiental:
        item = self._cadastros.get(codigo_cadastro_ambiental)
        if not item:
            raise CadastroAmbientalNotFoundError('Cadastro ambiental nao encontrado')
        item.validar(numero_processo)
        return item

    async def registrar_pendencia(self, codigo_cadastro_ambiental: str, *, pendencia: str) -> CadastroAmbiental:
        item = self._cadastros.get(codigo_cadastro_ambiental)
        if not item:
            raise CadastroAmbientalNotFoundError('Cadastro ambiental nao encontrado')
        item.adicionar_pendencia(pendencia)
        return item

    async def sanar_pendencias(self, codigo_cadastro_ambiental: str) -> CadastroAmbiental:
        item = self._cadastros.get(codigo_cadastro_ambiental)
        if not item:
            raise CadastroAmbientalNotFoundError('Cadastro ambiental nao encontrado')
        item.sanar_pendencias()
        return item

    async def obter_cadastro_ambiental(self, codigo_cadastro_ambiental: str) -> CadastroAmbiental:
        item = self._cadastros.get(codigo_cadastro_ambiental)
        if not item:
            raise CadastroAmbientalNotFoundError('Cadastro ambiental nao encontrado')
        return item

    async def listar_cadastros_ambientais(self, *, codigo_propriedade: str | None=None, status: StatusCadastroAmbiental | None=None) -> list[CadastroAmbiental]:
        values = list(self._cadastros.values())
        if codigo_propriedade:
            values = [item for item in values if item.codigo_propriedade == codigo_propriedade]
        if status:
            values = [item for item in values if item.status == status]
        return values