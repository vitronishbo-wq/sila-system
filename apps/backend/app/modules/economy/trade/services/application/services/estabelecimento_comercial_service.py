from __future__ import annotations
import logging
from datetime import date
from uuid import UUID
from app.modules.economy.trade.services.application.ports import EstabelecimentoComercialRepositoryPort
from app.modules.economy.trade.services.domain.enums import PorteComercial, RamoComercial, StatusComercial, TipoEstabelecimentoComercial, TipoRegimeTributario
from app.modules.economy.trade.services.domain.models import EstabelecimentoComercial
from app.modules.economy.trade.services.domain.shared import get_porte, get_ramo
from app.modules.economy.trade.services.exceptions import EstabelecimentoComercialAlreadyExistsError, EstabelecimentoComercialNotFoundError, InvalidEstabelecimentoComercialStateError
logger = logging.getLogger(__name__)

class EstabelecimentoComercialService:

    def __init__(self, *, repository: EstabelecimentoComercialRepositoryPort) -> None:
        self._repository = repository

    async def cadastrar(self, *, cnpj: str, razao_social: str, tipo: TipoEstabelecimentoComercial, ramo: RamoComercial, porte: PorteComercial, regime_tributario: TipoRegimeTributario, cnae_principal: str, data_abertura: date, endereco: str, numero: str, bairro: str, municipio: str, provincia: str, cep: str) -> EstabelecimentoComercial:
        existente = await self._repository.get_by_cnpj(cnpj)
        if existente:
            raise EstabelecimentoComercialAlreadyExistsError('Estabelecimento comercial ja cadastrado para o CNPJ informado')
        item = EstabelecimentoComercial.cadastrar(cnpj=cnpj, razao_social=razao_social, tipo=tipo, ramo=ramo, porte=porte, regime_tributario=regime_tributario, cnae_principal=cnae_principal, data_abertura=data_abertura, endereco=endereco, numero=numero, bairro=bairro, municipio=municipio, provincia=provincia, cep=cep)
        salvo = await self._repository.save(item)
        logger.info('comercio_servicos.estabelecimento.cadastrado id=%s cnpj=%s ramo=%s', str(salvo.id), salvo.cnpj, salvo.ramo.value)
        return salvo

    async def iniciar_atividades(self, id: UUID, *, data_inicio: date) -> EstabelecimentoComercial:
        item = await self._obter_ou_erro(id)
        try:
            item.iniciar_atividades(data_inicio)
        except ValueError as exc:
            raise InvalidEstabelecimentoComercialStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def suspender_atividades(self, id: UUID, *, motivo: str) -> EstabelecimentoComercial:
        item = await self._obter_ou_erro(id)
        try:
            item.suspender_atividades(motivo)
        except ValueError as exc:
            raise InvalidEstabelecimentoComercialStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def encerrar(self, id: UUID, *, data_encerramento: date, motivo: str) -> EstabelecimentoComercial:
        item = await self._obter_ou_erro(id)
        try:
            item.encerrar(data_encerramento=data_encerramento, motivo=motivo)
        except ValueError as exc:
            raise InvalidEstabelecimentoComercialStateError(str(exc)) from exc
        return await self._repository.save(item)

    async def associar_ramo(self, id: UUID, *, ramo: RamoComercial) -> EstabelecimentoComercial:
        item = await self._obter_ou_erro(id)
        item.associar_ramo(get_ramo(ramo))
        salvo = await self._repository.save(item)
        logger.info('comercio_servicos.estabelecimento.ramo id=%s ramo=%s', str(salvo.id), salvo.ramo.value)
        return salvo

    async def definir_porte(self, id: UUID, *, porte: PorteComercial) -> EstabelecimentoComercial:
        item = await self._obter_ou_erro(id)
        item.definir_porte(get_porte(porte))
        salvo = await self._repository.save(item)
        logger.info('comercio_servicos.estabelecimento.porte id=%s porte=%s', str(salvo.id), salvo.porte.value)
        return salvo

    async def obter_por_id(self, id: UUID) -> EstabelecimentoComercial:
        return await self._obter_ou_erro(id)

    async def listar(self, *, status: StatusComercial | None=None, ramo: RamoComercial | None=None, municipio: str | None=None) -> list[EstabelecimentoComercial]:
        return await self._repository.list(status=status, ramo=ramo, municipio=municipio)

    async def _obter_ou_erro(self, id: UUID) -> EstabelecimentoComercial:
        item = await self._repository.get_by_id(id)
        if not item:
            raise EstabelecimentoComercialNotFoundError('Estabelecimento comercial nao encontrado')
        return item