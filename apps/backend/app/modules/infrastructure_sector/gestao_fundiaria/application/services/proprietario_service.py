from __future__ import annotations

from decimal import Decimal

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.proprietario_repository_port import (
    ProprietarioRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import (
    TipoPessoa,
    TipoTitularidade,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.proprietario import (
    Proprietario,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.exceptions import (
    ProprietarioAlreadyExistsError,
    ProprietarioNotFoundError,
)


class ProprietarioService:
    def __init__(self, *, proprietario_repo: ProprietarioRepositoryPort) -> None:
        self._proprietario_repo = proprietario_repo

    async def cadastrar(
        self,
        *,
        nome: str,
        documento: str,
        tipo_pessoa: TipoPessoa,
        tipo_titularidade: TipoTitularidade,
        percentual_titularidade: Decimal | None = None,
        email: str | None = None,
        telefone: str | None = None,
        endereco: str | None = None,
    ) -> Proprietario:
        existente = await self._proprietario_repo.get_by_documento(documento.strip())
        if existente:
            raise ProprietarioAlreadyExistsError("Ja existe proprietario com este documento")
        item = Proprietario.cadastrar(
            nome=nome,
            documento=documento,
            tipo_pessoa=tipo_pessoa,
            tipo_titularidade=tipo_titularidade,
            numero_cadastro=await self._proprietario_repo.next_numero_cadastro(),
            percentual_titularidade=percentual_titularidade,
            email=email,
            telefone=telefone,
            endereco=endereco,
        )
        return await self._proprietario_repo.save(item)

    async def atualizar_contato(
        self,
        numero_cadastro: str,
        *,
        email: str | None = None,
        telefone: str | None = None,
        endereco: str | None = None,
    ) -> Proprietario:
        item = await self._obter_ou_erro(numero_cadastro)
        item.atualizar_contato(email=email, telefone=telefone, endereco=endereco)
        return await self._proprietario_repo.save(item)

    async def atualizar_titularidade(
        self,
        numero_cadastro: str,
        *,
        tipo_titularidade: TipoTitularidade,
        percentual_titularidade: Decimal | None = None,
    ) -> Proprietario:
        item = await self._obter_ou_erro(numero_cadastro)
        item.atualizar_titularidade(
            tipo_titularidade=tipo_titularidade, percentual_titularidade=percentual_titularidade
        )
        return await self._proprietario_repo.save(item)

    async def desativar(self, numero_cadastro: str, *, motivo: str) -> Proprietario:
        item = await self._obter_ou_erro(numero_cadastro)
        item.desativar(motivo)
        return await self._proprietario_repo.save(item)

    async def obter_por_numero_cadastro(self, numero_cadastro: str) -> Proprietario:
        return await self._obter_ou_erro(numero_cadastro)

    async def listar(
        self, *, tipo_pessoa: str | None = None, ativo: bool | None = None
    ) -> list[Proprietario]:
        return await self._proprietario_repo.list(tipo_pessoa=tipo_pessoa, ativo=ativo)

    async def _obter_ou_erro(self, numero_cadastro: str) -> Proprietario:
        item = await self._proprietario_repo.get_by_numero_cadastro(numero_cadastro)
        if not item:
            raise ProprietarioNotFoundError("Proprietario nao encontrado")
        return item
