from __future__ import annotations
from datetime import date
from app.modules.resources.agricultura.domain.enums import StatusEquipamento, TipoEquipamento
from app.modules.resources.agricultura.domain.models.equipamento import Equipamento
from app.modules.resources.agricultura.exceptions import EquipamentoNotFoundError

class EquipamentoService:

    def __init__(self) -> None:
        self._items: dict[str, Equipamento] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f'EQP/{date.today().year}/{self._seq:06d}'

    async def cadastrar(self, *, nome: str, tipo: TipoEquipamento, fabricante: str | None=None, modelo: str | None=None, ano_fabricacao: int | None=None, data_aquisicao: date | None=None) -> Equipamento:
        item = Equipamento.cadastrar(nome=nome, tipo=tipo, fabricante=fabricante, modelo=modelo, ano_fabricacao=ano_fabricacao, data_aquisicao=data_aquisicao)
        item.codigo_equipamento = self._next_codigo()
        self._items[item.codigo_equipamento] = item
        return item

    async def iniciar_uso(self, codigo_equipamento: str) -> Equipamento:
        item = self._items.get(codigo_equipamento)
        if not item:
            raise EquipamentoNotFoundError('Equipamento nao encontrado')
        item.iniciar_uso()
        return item

    async def registrar_uso(self, codigo_equipamento: str, *, horas: float) -> Equipamento:
        item = self._items.get(codigo_equipamento)
        if not item:
            raise EquipamentoNotFoundError('Equipamento nao encontrado')
        item.registrar_uso(horas)
        return item

    async def finalizar_uso(self, codigo_equipamento: str) -> Equipamento:
        item = self._items.get(codigo_equipamento)
        if not item:
            raise EquipamentoNotFoundError('Equipamento nao encontrado')
        item.finalizar_uso()
        return item

    async def enviar_manutencao(self, codigo_equipamento: str) -> Equipamento:
        item = self._items.get(codigo_equipamento)
        if not item:
            raise EquipamentoNotFoundError('Equipamento nao encontrado')
        item.enviar_manutencao()
        return item

    async def concluir_manutencao(self, codigo_equipamento: str) -> Equipamento:
        item = self._items.get(codigo_equipamento)
        if not item:
            raise EquipamentoNotFoundError('Equipamento nao encontrado')
        item.concluir_manutencao()
        return item

    async def inativar(self, codigo_equipamento: str) -> Equipamento:
        item = self._items.get(codigo_equipamento)
        if not item:
            raise EquipamentoNotFoundError('Equipamento nao encontrado')
        item.inativar()
        return item

    async def obter(self, codigo_equipamento: str) -> Equipamento:
        item = self._items.get(codigo_equipamento)
        if not item:
            raise EquipamentoNotFoundError('Equipamento nao encontrado')
        return item

    async def listar(self, *, status: StatusEquipamento | None=None, tipo: TipoEquipamento | None=None) -> list[Equipamento]:
        values = list(self._items.values())
        if status:
            values = [item for item in values if item.status == status]
        if tipo:
            values = [item for item in values if item.tipo == tipo]
        return values