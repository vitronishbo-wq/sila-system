from __future__ import annotations

from datetime import date
from uuid import UUID

from apps.backend.app.modules.public_security.application.ports.policial_repository_port import (
    PolicialRepositoryPort,
)
from apps.backend.app.modules.public_security.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.public_security.application.ports.unidade_policial_repository_port import (
    UnidadePolicialRepositoryPort,
)
from apps.backend.app.modules.public_security.domain.enums import (
    CargoPolicial,
    Patente,
    StatusAgente,
    TipoAgente,
    TipoVinculo,
)
from apps.backend.app.modules.public_security.domain.models.policial import Policial


class PolicialService:
    def __init__(
        self,
        *,
        policial_repo: PolicialRepositoryPort,
        unidade_repo: UnidadePolicialRepositoryPort,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.policial_repo = policial_repo
        self.unidade_repo = unidade_repo
        self.request_service = request_service

    async def cadastrar_policial(
        self,
        *,
        unidade_id: UUID,
        nome: str,
        data_nascimento: date,
        cpf: str,
        rg: str,
        tipo: TipoAgente,
        vinculo: TipoVinculo,
        cargo: CargoPolicial | None = None,
        patente: Patente | None = None,
        telefone: str | None = None,
        email: str | None = None,
        endereco: str | None = None,
        observacoes: str | None = None,
        citizen_id: UUID | None = None,
    ) -> Policial:
        unidade = await self.unidade_repo.get_by_id(unidade_id)
        if unidade is None:
            raise ValueError("Unidade policial nao encontrada")
        existente = await self.policial_repo.get_by_cpf(cpf)
        if existente is not None:
            raise ValueError("CPF ja cadastrado para outro policial")
        matricula = await self.policial_repo.next_matricula(unidade_id)
        policial = Policial.cadastrar(
            matricula=matricula,
            unidade_id=unidade_id,
            nome=nome,
            data_nascimento=data_nascimento,
            cpf=cpf,
            rg=rg,
            tipo=tipo,
            vinculo=vinculo,
            cargo=cargo,
            patente=patente,
            telefone=telefone,
            email=email,
            endereco=endereco,
            observacoes=observacoes,
        )
        saved = await self.policial_repo.save(policial)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_POLICIAL",
                entity_id=saved.id,
                citizen_id=citizen_id,
                numero_processo=saved.matricula,
                metadata={
                    "matricula": saved.matricula,
                    "nome": saved.nome,
                    "tipo": saved.tipo.value,
                    "unidade_codigo": unidade.codigo_unidade,
                },
            )
        return saved

    async def buscar_policial(self, policial_id: UUID) -> Policial:
        policial = await self.policial_repo.get_by_id(policial_id)
        if policial is None:
            raise ValueError("Policial nao encontrado")
        return policial

    async def listar_policiais(
        self,
        *,
        unidade_id: UUID | None = None,
        tipo: TipoAgente | None = None,
        status: StatusAgente | None = None,
    ) -> list[Policial]:
        if unidade_id is not None:
            return await self.policial_repo.list_by_unidade(unidade_id)
        if tipo is not None:
            return await self.policial_repo.list_by_tipo(tipo)
        if status is not None:
            return await self.policial_repo.list_by_status(status)
        return await self.policial_repo.list_all()

    async def atualizar_status(
        self, *, policial_id: UUID, status: StatusAgente, motivo: str | None = None
    ) -> Policial:
        policial = await self.buscar_policial(policial_id)
        policial.atualizar_status(status, motivo)
        return await self.policial_repo.save(policial)

    async def ativar_porte(
        self, *, policial_id: UUID, numero_porte: str, data_validade: date
    ) -> Policial:
        policial = await self.buscar_policial(policial_id)
        policial.ativar_porte(numero_porte=numero_porte, data_validade=data_validade)
        return await self.policial_repo.save(policial)

    async def remover_policial(self, policial_id: UUID) -> None:
        deleted = await self.policial_repo.delete(policial_id)
        if not deleted:
            raise ValueError("Policial nao encontrado")
