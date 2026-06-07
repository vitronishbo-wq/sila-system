from __future__ import annotations

from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.imovel_repository_port import (
    ImovelRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.justica_service_port import (
    JusticaServicePort,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.application.ports.matricula_imovel_repository_port import (
    MatriculaImovelRepositoryPort,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.enums import (
    StatusMatriculaImovel,
    TipoRegistro,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.domain.models.matricula_imovel import (
    MatriculaImovel,
)
from apps.backend.app.modules.infrastructure_sector.gestao_fundiaria.exceptions import (
    ImovelNotFoundError,
    MatriculaImovelAlreadyExistsError,
    MatriculaImovelNotFoundError,
)


class MatriculaImovelService:
    def __init__(
        self,
        *,
        matricula_repo: MatriculaImovelRepositoryPort,
        imovel_repo: ImovelRepositoryPort,
        justica_adapter: JusticaServicePort | None = None,
    ) -> None:
        self._matricula_repo = matricula_repo
        self._imovel_repo = imovel_repo
        self._justica_adapter = justica_adapter

    def has_justica_adapter(self) -> bool:
        return self._justica_adapter is not None

    async def registrar(
        self,
        *,
        imovel_inscricao: str,
        tipo_registro: TipoRegistro,
        cartorio_nome: str,
        livro: str,
        folha: str,
        comarca: str,
        provincia: str,
        proprietario_documento: str | None = None,
        numero_matricula: str | None = None,
    ) -> MatriculaImovel:
        imovel = await self._imovel_repo.get_by_inscricao(imovel_inscricao)
        if not imovel:
            raise ImovelNotFoundError("Imovel nao encontrado para registro da matricula")
        numero = numero_matricula or await self._matricula_repo.next_numero()
        existente = await self._matricula_repo.get_by_numero(numero)
        if existente:
            raise MatriculaImovelAlreadyExistsError("Ja existe matricula com este numero")
        if self._justica_adapter:
            valido = await self._justica_adapter.validar_matricula(
                numero_matricula=numero, cartorio_nome=cartorio_nome, livro=livro, folha=folha
            )
            if not valido:
                raise ValueError("Matricula invalida segundo o modulo Justica")
        matricula = MatriculaImovel.registrar(
            numero_matricula=numero,
            imovel_inscricao=imovel_inscricao,
            tipo_registro=tipo_registro,
            cartorio_nome=cartorio_nome,
            livro=livro,
            folha=folha,
            comarca=comarca,
            provincia=provincia,
            proprietario_documento=proprietario_documento,
        )
        matricula_salva = await self._matricula_repo.save(matricula)
        imovel.vincular_matricula(matricula_salva.id)
        await self._imovel_repo.save(imovel)
        return matricula_salva

    async def transferir(self, numero_matricula: str, *, novo_documento: str) -> MatriculaImovel:
        item = await self._obter_ou_erro(numero_matricula)
        item.transferir(novo_documento)
        return await self._matricula_repo.save(item)

    async def cancelar(self, numero_matricula: str, *, motivo: str) -> MatriculaImovel:
        item = await self._obter_ou_erro(numero_matricula)
        item.cancelar(motivo)
        return await self._matricula_repo.save(item)

    async def obter_por_numero(self, numero_matricula: str) -> MatriculaImovel:
        return await self._obter_ou_erro(numero_matricula)

    async def listar(
        self,
        *,
        imovel_inscricao: str | None = None,
        status: StatusMatriculaImovel | None = None,
        ativo: bool | None = None,
    ) -> list[MatriculaImovel]:
        return await self._matricula_repo.list(
            imovel_inscricao=imovel_inscricao, status=status, ativo=ativo
        )

    async def _obter_ou_erro(self, numero_matricula: str) -> MatriculaImovel:
        item = await self._matricula_repo.get_by_numero(numero_matricula)
        if not item:
            raise MatriculaImovelNotFoundError("Matricula nao encontrada")
        return item
