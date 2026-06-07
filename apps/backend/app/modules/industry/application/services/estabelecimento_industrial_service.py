from __future__ import annotations

import logging
from datetime import date
from uuid import UUID

from apps.backend.app.modules.industry.application.ports import (
    EstabelecimentoIndustrialRepositoryPort,
)
from apps.backend.app.modules.industry.domain.enums import (
    PorteIndustrial,
    RamoIndustrial,
    StatusEstabelecimento,
    TipoEstabelecimento,
)
from apps.backend.app.modules.industry.domain.exceptions import (
    EstabelecimentoIndustrialAlreadyExistsError,
    EstabelecimentoIndustrialNotFoundError,
    InvalidEstabelecimentoIndustrialStateError,
)
from apps.backend.app.modules.industry.domain.models import EstabelecimentoIndustrial
from apps.backend.app.modules.industry.domain.shared import get_porte, get_ramo

logger = logging.getLogger(__name__)


class EstabelecimentoIndustrialService:
    def __init__(self, *, repository: EstabelecimentoIndustrialRepositoryPort) -> None:
        self._repository = repository

    async def cadastrar(
        self,
        *,
        cnpj: str,
        razao_social: str,
        ramo: RamoIndustrial,
        porte: PorteIndustrial,
        tipo: TipoEstabelecimento,
        cnae_principal: str,
        data_abertura: date,
        endereco: str,
        bairro: str,
        municipio: str,
        provincia: str,
    ) -> EstabelecimentoIndustrial:
        existente = await self._repository.get_by_cnpj(cnpj)
        if existente:
            raise EstabelecimentoIndustrialAlreadyExistsError(
                "Estabelecimento industrial ja cadastrado para o CNPJ informado"
            )
        item = EstabelecimentoIndustrial.cadastrar(
            cnpj=cnpj,
            razao_social=razao_social,
            ramo=ramo,
            porte=porte,
            tipo=tipo,
            cnae_principal=cnae_principal,
            data_abertura=data_abertura,
            endereco=endereco,
            bairro=bairro,
            municipio=municipio,
            provincia=provincia,
        )
        salvo = await self._repository.save(item)
        logger.info(
            "industria.estabelecimento.cadastrado id=%s cnpj=%s ramo=%s porte=%s",
            str(salvo.id),
            salvo.cnpj,
            salvo.ramo.value,
            salvo.porte.value,
        )
        return salvo

    async def iniciar_atividades(self, id: UUID, *, data_inicio: date) -> EstabelecimentoIndustrial:
        item = await self._obter_ou_erro(id)
        try:
            item.iniciar_atividades(data_inicio)
        except ValueError as exc:
            raise InvalidEstabelecimentoIndustrialStateError(str(exc)) from exc
        salvo = await self._repository.save(item)
        logger.info(
            "industria.estabelecimento.status id=%s status=%s acao=iniciar_atividades",
            str(salvo.id),
            salvo.status.value,
        )
        return salvo

    async def suspender_atividades(self, id: UUID, *, motivo: str) -> EstabelecimentoIndustrial:
        item = await self._obter_ou_erro(id)
        try:
            item.suspender_atividades(motivo)
        except ValueError as exc:
            raise InvalidEstabelecimentoIndustrialStateError(str(exc)) from exc
        salvo = await self._repository.save(item)
        logger.info(
            "industria.estabelecimento.status id=%s status=%s acao=suspender_atividades",
            str(salvo.id),
            salvo.status.value,
        )
        return salvo

    async def paralisar(self, id: UUID, *, motivo: str) -> EstabelecimentoIndustrial:
        item = await self._obter_ou_erro(id)
        try:
            item.paralisar(motivo)
        except ValueError as exc:
            raise InvalidEstabelecimentoIndustrialStateError(str(exc)) from exc
        salvo = await self._repository.save(item)
        logger.info(
            "industria.estabelecimento.status id=%s status=%s acao=paralisar",
            str(salvo.id),
            salvo.status.value,
        )
        return salvo

    async def reativar(self, id: UUID) -> EstabelecimentoIndustrial:
        item = await self._obter_ou_erro(id)
        try:
            item.reativar()
        except ValueError as exc:
            raise InvalidEstabelecimentoIndustrialStateError(str(exc)) from exc
        salvo = await self._repository.save(item)
        logger.info(
            "industria.estabelecimento.status id=%s status=%s acao=reativar",
            str(salvo.id),
            salvo.status.value,
        )
        return salvo

    async def associar_ramo(self, id: UUID, *, ramo: RamoIndustrial) -> EstabelecimentoIndustrial:
        item = await self._obter_ou_erro(id)
        item.associar_ramo(get_ramo(ramo))
        salvo = await self._repository.save(item)
        logger.info("industria.estabelecimento.ramo id=%s ramo=%s", str(salvo.id), salvo.ramo.value)
        return salvo

    async def definir_porte(self, id: UUID, *, porte: PorteIndustrial) -> EstabelecimentoIndustrial:
        item = await self._obter_ou_erro(id)
        item.definir_porte(get_porte(porte))
        salvo = await self._repository.save(item)
        logger.info(
            "industria.estabelecimento.porte id=%s porte=%s", str(salvo.id), salvo.porte.value
        )
        return salvo

    async def obter_por_id(self, id: UUID) -> EstabelecimentoIndustrial:
        return await self._obter_ou_erro(id)

    async def listar(
        self,
        *,
        status: StatusEstabelecimento | None = None,
        ramo: RamoIndustrial | None = None,
        municipio: str | None = None,
    ) -> list[EstabelecimentoIndustrial]:
        return await self._repository.list(status=status, ramo=ramo, municipio=municipio)

    async def _obter_ou_erro(self, id: UUID) -> EstabelecimentoIndustrial:
        item = await self._repository.get_by_id(id)
        if not item:
            raise EstabelecimentoIndustrialNotFoundError(
                "Estabelecimento industrial nao encontrado"
            )
        return item
