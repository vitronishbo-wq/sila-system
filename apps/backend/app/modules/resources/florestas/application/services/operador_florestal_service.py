from __future__ import annotations
from app.modules.resources.florestas.application.ports.concessionario_florestal_repository_port import ConcessionarioFlorestalRepositoryPort
from app.modules.resources.florestas.domain.enums import TipoOperadorFlorestal
from app.modules.resources.florestas.domain.models.concessionario_florestal import ConcessionarioFlorestal

class OperadorFlorestalService:

    def __init__(self, repository: ConcessionarioFlorestalRepositoryPort):
        self.repository = repository

    async def cadastrar_operador(self, *, nome: str, nif: str, tipo_operador: TipoOperadorFlorestal=TipoOperadorFlorestal.EMPRESA) -> ConcessionarioFlorestal:
        if await self.repository.get_by_nif(nif):
            raise ValueError('Operador com este NIF ja existe')
        operador = ConcessionarioFlorestal.cadastrar(nome=nome, nif=nif, tipo_operador=tipo_operador)
        return await self.repository.save(operador)

    async def obter_operador(self, operador_id):
        item = await self.repository.get_by_id(operador_id)
        if not item:
            raise ValueError('Operador florestal nao encontrado')
        return item

    async def listar_operadores(self, *, ativo: bool | None=None) -> list[ConcessionarioFlorestal]:
        return await self.repository.list_all(ativo)