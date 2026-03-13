from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.resources.aguas_saneamento.application.ports.abastecimento_repository_port import AbastecimentoRepositoryPort
from apps.backend.app.modules.resources.aguas_saneamento.domain.enums import StatusAbastecimento
from apps.backend.app.modules.resources.aguas_saneamento.domain.models.abastecimento import AbastecimentoAgua
from apps.backend.app.modules.resources.aguas_saneamento.exceptions import AbastecimentoAlreadyExistsError, AbastecimentoNotFoundError

class AbastecimentoService:

    def __init__(self, *, abastecimento_repo: AbastecimentoRepositoryPort) -> None:
        self._abastecimento_repo = abastecimento_repo

    async def registrar(self, *, infraestrutura_id: UUID, nome_sistema: str, provincia: str, municipio: str) -> AbastecimentoAgua:
        existentes = await self._abastecimento_repo.list(infraestrutura_id=infraestrutura_id, provincia=provincia.strip(), municipio=municipio.strip())
        ativos = {StatusAbastecimento.PLANEJADO, StatusAbastecimento.OPERACIONAL, StatusAbastecimento.INTERROMPIDO}
        if any((item.nome_sistema.lower() == nome_sistema.strip().lower() and item.status in ativos for item in existentes)):
            raise AbastecimentoAlreadyExistsError('Ja existe sistema de abastecimento equivalente')
        item = AbastecimentoAgua.registrar(infraestrutura_id=infraestrutura_id, nome_sistema=nome_sistema, provincia=provincia, municipio=municipio)
        item.codigo_abastecimento = await self._abastecimento_repo.next_codigo()
        return await self._abastecimento_repo.save(item)

    async def iniciar_operacao(self, codigo_abastecimento: str, *, data_inicio_operacao: date | None=None) -> AbastecimentoAgua:
        item = await self._obter_ou_erro(codigo_abastecimento)
        item.iniciar_operacao(data_inicio_operacao=data_inicio_operacao)
        return await self._abastecimento_repo.save(item)

    async def interromper(self, codigo_abastecimento: str, *, motivo: str) -> AbastecimentoAgua:
        item = await self._obter_ou_erro(codigo_abastecimento)
        item.interromper(motivo)
        return await self._abastecimento_repo.save(item)

    async def retomar(self, codigo_abastecimento: str) -> AbastecimentoAgua:
        item = await self._obter_ou_erro(codigo_abastecimento)
        item.retomar()
        return await self._abastecimento_repo.save(item)

    async def encerrar(self, codigo_abastecimento: str, *, motivo: str) -> AbastecimentoAgua:
        item = await self._obter_ou_erro(codigo_abastecimento)
        item.encerrar(motivo)
        return await self._abastecimento_repo.save(item)

    async def obter_por_codigo(self, codigo_abastecimento: str) -> AbastecimentoAgua:
        return await self._obter_ou_erro(codigo_abastecimento)

    async def listar(self, *, infraestrutura_id: UUID | None=None, status: StatusAbastecimento | None=None, provincia: str | None=None, municipio: str | None=None) -> list[AbastecimentoAgua]:
        return await self._abastecimento_repo.list(infraestrutura_id=infraestrutura_id, status=status, provincia=provincia, municipio=municipio)

    async def _obter_ou_erro(self, codigo_abastecimento: str) -> AbastecimentoAgua:
        item = await self._abastecimento_repo.get_by_codigo(codigo_abastecimento)
        if not item:
            raise AbastecimentoNotFoundError('Abastecimento nao encontrado')
        return item