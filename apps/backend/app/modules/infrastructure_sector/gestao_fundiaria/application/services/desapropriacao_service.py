from __future__ import annotations
from datetime import date
from decimal import Decimal
from app.modules.infrastructure_sector.gestao_fundiaria.application.ports.ambiente_service_port import AmbienteServicePort
from app.modules.infrastructure_sector.gestao_fundiaria.application.ports.desapropriacao_repository_port import DesapropriacaoRepositoryPort
from app.modules.infrastructure_sector.gestao_fundiaria.application.ports.imovel_repository_port import ImovelRepositoryPort
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import StatusDesapropriacao, TipoDesapropriacao
from app.modules.infrastructure_sector.gestao_fundiaria.domain.models.desapropriacao import Desapropriacao
from app.modules.infrastructure_sector.gestao_fundiaria.exceptions import DesapropriacaoAlreadyExistsError, DesapropriacaoNotFoundError, ImovelNotFoundError

class DesapropriacaoService:

    def __init__(self, *, desapropriacao_repo: DesapropriacaoRepositoryPort, imovel_repo: ImovelRepositoryPort, ambiente_adapter: AmbienteServicePort | None=None) -> None:
        self._desapropriacao_repo = desapropriacao_repo
        self._imovel_repo = imovel_repo
        self._ambiente_adapter = ambiente_adapter

    def has_ambiente_adapter(self) -> bool:
        return self._ambiente_adapter is not None

    async def instaurar(self, *, imovel_inscricao: str, tipo: TipoDesapropriacao, ente_publico: str, finalidade: str, valor_indenizacao: Decimal, numero_processo: str | None=None) -> Desapropriacao:
        imovel = await self._imovel_repo.get_by_inscricao(imovel_inscricao)
        if not imovel:
            raise ImovelNotFoundError('Imovel nao encontrado para desapropriacao')
        if tipo == TipoDesapropriacao.REFORMA_AGRARIA and self._ambiente_adapter:
            car_valido = await self._ambiente_adapter.validar_car(imovel.id)
            if not car_valido:
                raise ValueError('Imovel sem validacao ambiental para reforma agraria')
        numero = numero_processo or await self._desapropriacao_repo.next_numero_processo()
        existente = await self._desapropriacao_repo.get_by_numero_processo(numero)
        if existente:
            raise DesapropriacaoAlreadyExistsError('Ja existe desapropriacao com este numero de processo')
        processo = Desapropriacao.instaurar(numero_processo=numero, imovel_inscricao=imovel_inscricao, tipo=tipo, ente_publico=ente_publico, finalidade=finalidade, valor_indenizacao=valor_indenizacao)
        return await self._desapropriacao_repo.save(processo)

    async def decretar(self, numero_processo: str, *, data_decreto: date) -> Desapropriacao:
        item = await self._obter_ou_erro(numero_processo)
        item.decretar(data_decreto)
        return await self._desapropriacao_repo.save(item)

    async def registrar_pagamento(self, numero_processo: str, *, data_pagamento: date | None=None) -> Desapropriacao:
        item = await self._obter_ou_erro(numero_processo)
        item.registrar_pagamento(data_pagamento)
        return await self._desapropriacao_repo.save(item)

    async def encerrar(self, numero_processo: str, *, motivo: str) -> Desapropriacao:
        item = await self._obter_ou_erro(numero_processo)
        item.encerrar(motivo)
        return await self._desapropriacao_repo.save(item)

    async def cancelar(self, numero_processo: str, *, motivo: str) -> Desapropriacao:
        item = await self._obter_ou_erro(numero_processo)
        item.cancelar(motivo)
        return await self._desapropriacao_repo.save(item)

    async def obter_por_numero_processo(self, numero_processo: str) -> Desapropriacao:
        return await self._obter_ou_erro(numero_processo)

    async def listar(self, *, imovel_inscricao: str | None=None, status: StatusDesapropriacao | None=None, ativo: bool | None=None) -> list[Desapropriacao]:
        return await self._desapropriacao_repo.list(imovel_inscricao=imovel_inscricao, status=status, ativo=ativo)

    async def _obter_ou_erro(self, numero_processo: str) -> Desapropriacao:
        item = await self._desapropriacao_repo.get_by_numero_processo(numero_processo)
        if not item:
            raise DesapropriacaoNotFoundError('Desapropriacao nao encontrada')
        return item