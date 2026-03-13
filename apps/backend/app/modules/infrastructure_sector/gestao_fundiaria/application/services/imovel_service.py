from __future__ import annotations
from decimal import Decimal
from uuid import UUID
from app.modules.infrastructure_sector.gestao_fundiaria.application.ports.imovel_repository_port import ImovelRepositoryPort
from app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import NaturezaImovel, SituacaoDominial, TipoImovel
from app.modules.infrastructure_sector.gestao_fundiaria.domain.models.imovel import Imovel
from app.modules.infrastructure_sector.gestao_fundiaria.exceptions import ImovelAlreadyExistsError, ImovelNotFoundError

class ImovelService:

    def __init__(self, *, imovel_repo: ImovelRepositoryPort) -> None:
        self._imovel_repo = imovel_repo

    async def cadastrar(self, *, tipo: TipoImovel, natureza: NaturezaImovel, area_total: Decimal, endereco: str, bairro: str, municipio: str, provincia: str, inscricao_imobiliaria: str | None=None) -> Imovel:
        inscricao = inscricao_imobiliaria or await self._imovel_repo.next_inscricao()
        existente = await self._imovel_repo.get_by_inscricao(inscricao)
        if existente:
            raise ImovelAlreadyExistsError('Ja existe imovel com esta inscricao imobiliaria')
        item = Imovel.cadastrar(tipo=tipo, natureza=natureza, area_total=area_total, endereco=endereco, bairro=bairro, municipio=municipio, provincia=provincia, inscricao_imobiliaria=inscricao)
        return await self._imovel_repo.save(item)

    async def atualizar_area(self, inscricao_imobiliaria: str, *, area_total: Decimal) -> Imovel:
        item = await self._obter_ou_erro(inscricao_imobiliaria)
        item.atualizar_area(area_total)
        return await self._imovel_repo.save(item)

    async def atualizar_proprietario(self, inscricao_imobiliaria: str, *, proprietario_id: UUID) -> Imovel:
        item = await self._obter_ou_erro(inscricao_imobiliaria)
        item.atualizar_proprietario(proprietario_id)
        return await self._imovel_repo.save(item)

    async def atualizar_situacao(self, inscricao_imobiliaria: str, *, situacao: SituacaoDominial) -> Imovel:
        item = await self._obter_ou_erro(inscricao_imobiliaria)
        item.atualizar_situacao(situacao)
        return await self._imovel_repo.save(item)

    async def vincular_matricula(self, inscricao_imobiliaria: str, *, matricula_id: UUID) -> Imovel:
        item = await self._obter_ou_erro(inscricao_imobiliaria)
        item.vincular_matricula(matricula_id)
        return await self._imovel_repo.save(item)

    async def desativar(self, inscricao_imobiliaria: str, *, motivo: str) -> Imovel:
        item = await self._obter_ou_erro(inscricao_imobiliaria)
        item.desativar(motivo)
        return await self._imovel_repo.save(item)

    async def obter_por_inscricao(self, inscricao_imobiliaria: str) -> Imovel:
        return await self._obter_ou_erro(inscricao_imobiliaria)

    async def listar(self, *, proprietario_atual_id: UUID | None=None, municipio: str | None=None, provincia: str | None=None, ativo: bool | None=None) -> list[Imovel]:
        return await self._imovel_repo.list(proprietario_atual_id=proprietario_atual_id, municipio=municipio, provincia=provincia, ativo=ativo)

    async def _obter_ou_erro(self, inscricao_imobiliaria: str) -> Imovel:
        item = await self._imovel_repo.get_by_inscricao(inscricao_imobiliaria)
        if not item:
            raise ImovelNotFoundError('Imovel nao encontrado')
        return item