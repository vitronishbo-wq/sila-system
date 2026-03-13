from __future__ import annotations
from datetime import date
from decimal import Decimal
from uuid import UUID
from app.modules.resources.aguas_saneamento.application.ports.infraestrutura_repository_port import InfraestruturaRepositoryPort
from app.modules.resources.aguas_saneamento.domain.enums import StatusInfraestrutura, TipoInfraestrutura
from app.modules.resources.aguas_saneamento.domain.models.infraestrutura import InfraestruturaHidrica
from app.modules.resources.aguas_saneamento.exceptions import InfraestruturaAlreadyExistsError, InfraestruturaNotFoundError

class InfraestruturaService:

    def __init__(self, *, infraestrutura_repo: InfraestruturaRepositoryPort) -> None:
        self._infraestrutura_repo = infraestrutura_repo

    async def registrar(self, *, tipo: TipoInfraestrutura, nome: str, provincia: str, municipio: str, capacidade: Decimal | None=None, unidade_capacidade: str | None=None, outorga_id: UUID | None=None, latitude: Decimal | None=None, longitude: Decimal | None=None) -> InfraestruturaHidrica:
        existentes = await self._infraestrutura_repo.list(tipo=tipo, provincia=provincia.strip(), municipio=municipio.strip())
        ativos = {StatusInfraestrutura.PLANEJADA, StatusInfraestrutura.OPERACIONAL, StatusInfraestrutura.MANUTENCAO, StatusInfraestrutura.INTERDITADA}
        if any((item.nome.lower() == nome.strip().lower() and item.status in ativos for item in existentes)):
            raise InfraestruturaAlreadyExistsError('Ja existe infraestrutura equivalente registrada')
        item = InfraestruturaHidrica.registrar(tipo=tipo, nome=nome, provincia=provincia, municipio=municipio, capacidade=capacidade, unidade_capacidade=unidade_capacidade, outorga_id=outorga_id, latitude=latitude, longitude=longitude)
        item.codigo_infraestrutura = await self._infraestrutura_repo.next_codigo()
        return await self._infraestrutura_repo.save(item)

    async def ativar(self, codigo_infraestrutura: str, *, data_operacao: date | None=None) -> InfraestruturaHidrica:
        item = await self._obter_ou_erro(codigo_infraestrutura)
        item.ativar(data_operacao=data_operacao)
        return await self._infraestrutura_repo.save(item)

    async def manutencao(self, codigo_infraestrutura: str, *, motivo: str) -> InfraestruturaHidrica:
        item = await self._obter_ou_erro(codigo_infraestrutura)
        item.colocar_em_manutencao(motivo)
        return await self._infraestrutura_repo.save(item)

    async def interditar(self, codigo_infraestrutura: str, *, motivo: str) -> InfraestruturaHidrica:
        item = await self._obter_ou_erro(codigo_infraestrutura)
        item.interditar(motivo)
        return await self._infraestrutura_repo.save(item)

    async def reativar(self, codigo_infraestrutura: str, *, motivo: str | None=None) -> InfraestruturaHidrica:
        item = await self._obter_ou_erro(codigo_infraestrutura)
        item.reativar(motivo)
        return await self._infraestrutura_repo.save(item)

    async def desativar(self, codigo_infraestrutura: str, *, motivo: str) -> InfraestruturaHidrica:
        item = await self._obter_ou_erro(codigo_infraestrutura)
        item.desativar(motivo)
        return await self._infraestrutura_repo.save(item)

    async def obter_por_codigo(self, codigo_infraestrutura: str) -> InfraestruturaHidrica:
        return await self._obter_ou_erro(codigo_infraestrutura)

    async def listar(self, *, tipo: TipoInfraestrutura | None=None, status: StatusInfraestrutura | None=None, provincia: str | None=None, municipio: str | None=None) -> list[InfraestruturaHidrica]:
        return await self._infraestrutura_repo.list(tipo=tipo, status=status, provincia=provincia, municipio=municipio)

    async def _obter_ou_erro(self, codigo_infraestrutura: str) -> InfraestruturaHidrica:
        item = await self._infraestrutura_repo.get_by_codigo(codigo_infraestrutura)
        if not item:
            raise InfraestruturaNotFoundError('Infraestrutura nao encontrada')
        return item