from __future__ import annotations
from datetime import date
from app.modules.resources.agricultura.application.services.propriedade_service import PropriedadeService
from app.modules.resources.agricultura.domain.models.certificacao import Certificacao
from app.modules.resources.agricultura.exceptions import CertificacaoNotFoundError

class CertificacaoService:

    def __init__(self, *, propriedade_service: PropriedadeService) -> None:
        self._propriedade_service = propriedade_service
        self._items: dict[str, Certificacao] = {}
        self._seq = 0

    def _next_codigo(self) -> str:
        self._seq += 1
        return f'CER/{date.today().year}/{self._seq:06d}'

    async def solicitar(self, *, codigo_propriedade: str, tipo: str, orgao_emissor: str) -> Certificacao:
        await self._propriedade_service.obter(codigo_propriedade)
        item = Certificacao.solicitar(codigo_propriedade=codigo_propriedade, tipo=tipo, orgao_emissor=orgao_emissor)
        item.codigo_certificacao = self._next_codigo()
        self._items[item.codigo_certificacao] = item
        return item

    async def aprovar(self, codigo_certificacao: str, *, data_validade: date | None=None) -> Certificacao:
        item = self._items.get(codigo_certificacao)
        if not item:
            raise CertificacaoNotFoundError('Certificacao nao encontrada')
        item.aprovar(data_validade=data_validade)
        return item

    async def reprovar(self, codigo_certificacao: str, *, motivo: str) -> Certificacao:
        item = self._items.get(codigo_certificacao)
        if not item:
            raise CertificacaoNotFoundError('Certificacao nao encontrada')
        item.reprovar(motivo)
        return item

    async def obter(self, codigo_certificacao: str) -> Certificacao:
        item = self._items.get(codigo_certificacao)
        if not item:
            raise CertificacaoNotFoundError('Certificacao nao encontrada')
        return item

    async def listar(self, *, codigo_propriedade: str | None=None) -> list[Certificacao]:
        values = list(self._items.values())
        if codigo_propriedade:
            values = [item for item in values if item.codigo_propriedade == codigo_propriedade]
        return values