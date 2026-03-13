from __future__ import annotations
from datetime import date
from apps.backend.app.modules.resources.ambiente.application.ports.fiscalizacao_repository_port import FiscalizacaoRepositoryPort
from apps.backend.app.modules.resources.ambiente.application.ports.licenca_repository_port import LicencaRepositoryPort
from apps.backend.app.modules.resources.ambiente.domain.enums import StatusFiscalizacao, StatusLicenca
from apps.backend.app.modules.resources.ambiente.domain.models.fiscalizacao import Fiscalizacao
from apps.backend.app.modules.resources.ambiente.exceptions import FiscalizacaoNotFoundError, LicencaNotFoundError

class FiscalizacaoService:

    def __init__(self, *, licenca_repo: LicencaRepositoryPort, fiscalizacao_repo: FiscalizacaoRepositoryPort) -> None:
        self._licenca_repo = licenca_repo
        self._fiscalizacao_repo = fiscalizacao_repo

    async def agendar(self, *, numero_licenca: str, localidade: str, objetivo: str, fiscal_responsavel: str, data_agendada: date) -> Fiscalizacao:
        licenca = await self._licenca_repo.get_by_numero(numero_licenca)
        if not licenca:
            raise LicencaNotFoundError('Licenca ambiental nao encontrada')
        if licenca.status != StatusLicenca.DEFERIDA:
            raise ValueError('Licenca precisa estar deferida para agendar fiscalizacao')
        item = Fiscalizacao.agendar(numero_licenca=numero_licenca, localidade=localidade, objetivo=objetivo, fiscal_responsavel=fiscal_responsavel, data_agendada=data_agendada)
        item.numero_fiscalizacao = await self._fiscalizacao_repo.next_numero()
        return await self._fiscalizacao_repo.save(item)

    async def iniciar(self, numero_fiscalizacao: str) -> Fiscalizacao:
        item = await self._fiscalizacao_repo.get_by_numero(numero_fiscalizacao)
        if not item:
            raise FiscalizacaoNotFoundError('Fiscalizacao nao encontrada')
        item.iniciar()
        return await self._fiscalizacao_repo.save(item)

    async def concluir(self, numero_fiscalizacao: str, relatorio: str) -> Fiscalizacao:
        item = await self._fiscalizacao_repo.get_by_numero(numero_fiscalizacao)
        if not item:
            raise FiscalizacaoNotFoundError('Fiscalizacao nao encontrada')
        item.concluir(relatorio)
        return await self._fiscalizacao_repo.save(item)

    async def cancelar(self, numero_fiscalizacao: str, motivo: str) -> Fiscalizacao:
        item = await self._fiscalizacao_repo.get_by_numero(numero_fiscalizacao)
        if not item:
            raise FiscalizacaoNotFoundError('Fiscalizacao nao encontrada')
        item.cancelar(motivo)
        return await self._fiscalizacao_repo.save(item)

    async def obter_por_numero(self, numero_fiscalizacao: str) -> Fiscalizacao:
        item = await self._fiscalizacao_repo.get_by_numero(numero_fiscalizacao)
        if not item:
            raise FiscalizacaoNotFoundError('Fiscalizacao nao encontrada')
        return item

    async def listar(self, *, numero_licenca: str | None=None, status: StatusFiscalizacao | None=None) -> list[Fiscalizacao]:
        return await self._fiscalizacao_repo.list(numero_licenca=numero_licenca, status=status)