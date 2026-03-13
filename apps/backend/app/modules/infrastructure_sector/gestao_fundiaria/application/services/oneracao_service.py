from __future__ import annotations
from datetime import date
from decimal import Decimal
from app.modules.infrastructure_sector.gestao_fundiaria.application.ports.imovel_repository_port import ImovelRepositoryPort
from app.modules.infrastructure_sector.gestao_fundiaria.application.ports.justica_service_port import JusticaServicePort
from app.modules.infrastructure_sector.gestao_fundiaria.application.ports.oneracao_repository_port import OneracaoRepositoryPort
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusOneracao, TipoOneracao
from app.modules.infrastructure_sector.gestao_fundiaria.domain.models.oneracao import Oneracao
from app.modules.infrastructure_sector.gestao_fundiaria.exceptions import ImovelNotFoundError, OneracaoAlreadyExistsError, OneracaoNotFoundError

class OneracaoService:

    def __init__(self, *, oneracao_repo: OneracaoRepositoryPort, imovel_repo: ImovelRepositoryPort, justica_adapter: JusticaServicePort | None=None) -> None:
        self._oneracao_repo = oneracao_repo
        self._imovel_repo = imovel_repo
        self._justica_adapter = justica_adapter

    def has_justica_adapter(self) -> bool:
        return self._justica_adapter is not None

    async def registrar(self, *, imovel_inscricao: str, tipo: TipoOneracao, credor_nome: str, valor: Decimal, documento_credor: str | None=None, data_vencimento: date | None=None, descricao: str | None=None, numero_oneracao: str | None=None) -> Oneracao:
        imovel = await self._imovel_repo.get_by_inscricao(imovel_inscricao)
        if not imovel:
            raise ImovelNotFoundError('Imovel nao encontrado para registrar oneracao')
        if tipo == TipoOneracao.PENHORA and self._justica_adapter:
            litigio_ativo = await self._justica_adapter.possui_litigio_ativo(imovel.id)
            if not litigio_ativo:
                raise ValueError('Penhora exige litigio ativo no modulo Justica')
        numero = numero_oneracao or await self._oneracao_repo.next_numero()
        existente = await self._oneracao_repo.get_by_numero(numero)
        if existente:
            raise OneracaoAlreadyExistsError('Ja existe oneracao com este numero')
        oneracao = Oneracao.registrar(numero_oneracao=numero, imovel_inscricao=imovel_inscricao, tipo=tipo, credor_nome=credor_nome, valor=valor, documento_credor=documento_credor, data_vencimento=data_vencimento, descricao=descricao)
        return await self._oneracao_repo.save(oneracao)

    async def baixar(self, numero_oneracao: str, *, motivo: str) -> Oneracao:
        item = await self._obter_ou_erro(numero_oneracao)
        item.baixar(motivo)
        return await self._oneracao_repo.save(item)

    async def cancelar(self, numero_oneracao: str, *, motivo: str) -> Oneracao:
        item = await self._obter_ou_erro(numero_oneracao)
        item.cancelar(motivo)
        return await self._oneracao_repo.save(item)

    async def obter_por_numero(self, numero_oneracao: str) -> Oneracao:
        return await self._obter_ou_erro(numero_oneracao)

    async def listar(self, *, imovel_inscricao: str | None=None, status: StatusOneracao | None=None, ativo: bool | None=None) -> list[Oneracao]:
        return await self._oneracao_repo.list(imovel_inscricao=imovel_inscricao, status=status, ativo=ativo)

    async def _obter_ou_erro(self, numero_oneracao: str) -> Oneracao:
        item = await self._oneracao_repo.get_by_numero(numero_oneracao)
        if not item:
            raise OneracaoNotFoundError('Oneracao nao encontrada')
        return item