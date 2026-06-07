from __future__ import annotations

from datetime import date
from decimal import Decimal
from uuid import UUID

from apps.backend.app.modules.society.desporto.application.ports.atleta_repository_port import (
    AtletaRepositoryPort,
)
from apps.backend.app.modules.society.desporto.application.ports.citizen_service_port import (
    CitizenServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.request_service_port import (
    RequestServicePort,
)
from apps.backend.app.modules.society.desporto.application.ports.saude_service_port import (
    SaudeServicePort,
)
from apps.backend.app.modules.society.desporto.domain.enums import (
    ModalidadeDesportiva,
    PePreferencial,
    PosicaoAtleta,
    StatusAtleta,
    TipoAtleta,
)
from apps.backend.app.modules.society.desporto.domain.models.atleta import Atleta


class AtletaService:
    def __init__(
        self,
        *,
        atleta_repo: AtletaRepositoryPort,
        citizen_service: CitizenServicePort | None = None,
        saude_service: SaudeServicePort | None = None,
        request_service: RequestServicePort | None = None,
    ) -> None:
        self.atleta_repo = atleta_repo
        self.citizen_service = citizen_service
        self.saude_service = saude_service
        self.request_service = request_service

    async def cadastrar_atleta(
        self,
        *,
        nome: str,
        data_nascimento: date,
        naturalidade: str,
        nacionalidade: str,
        tipo: TipoAtleta,
        modalidades: list[ModalidadeDesportiva],
        citizen_id: UUID | None = None,
        posicoes: list[PosicaoAtleta] | None = None,
        pe_preferencial: PePreferencial | None = None,
        altura_cm: int | None = None,
        peso_kg: Decimal | None = None,
        clube_atual_id: UUID | None = None,
        numero_camisola: int | None = None,
        ultimo_exame_id: UUID | None = None,
        observacoes: str | None = None,
    ) -> Atleta:
        if citizen_id is not None and self.citizen_service is not None:
            ativo = await self.citizen_service.is_citizen_active(citizen_id)
            if not ativo:
                raise ValueError("Cidadao nao encontrado ou inativo")
        if ultimo_exame_id is not None and self.saude_service is not None:
            exame_ok = await self.saude_service.exame_exists(ultimo_exame_id)
            if not exame_ok:
                raise ValueError("Exame medico informado nao encontrado")
        registro = await self.atleta_repo.next_registro()
        atleta = Atleta.cadastrar(
            numero_registro=registro,
            nome=nome,
            data_nascimento=data_nascimento,
            naturalidade=naturalidade,
            nacionalidade=nacionalidade,
            tipo=tipo,
            modalidades=modalidades,
            citizen_id=citizen_id,
            posicoes=posicoes,
            pe_preferencial=pe_preferencial,
            altura_cm=altura_cm,
            peso_kg=peso_kg,
            clube_atual_id=clube_atual_id,
            numero_camisola=numero_camisola,
            ultimo_exame_id=ultimo_exame_id,
            observacoes=observacoes,
        )
        saved = await self.atleta_repo.save(atleta)
        if self.request_service is not None:
            await self.request_service.create_request(
                request_type="CADASTRO_ATLETA",
                entity_id=saved.id,
                citizen_id=citizen_id,
                metadata={
                    "registro": saved.numero_registro,
                    "nome": saved.nome,
                    "tipo": saved.tipo.value,
                    "modalidades": [item.value for item in saved.modalidades],
                },
                numero_processo=saved.numero_registro,
            )
        return saved

    async def buscar_atleta(self, atleta_id: UUID) -> Atleta:
        item = await self.atleta_repo.get_by_id(atleta_id)
        if item is None:
            raise ValueError("Atleta nao encontrado")
        return item

    async def listar_atletas(
        self,
        *,
        tipo: TipoAtleta | None = None,
        modalidade: ModalidadeDesportiva | None = None,
        status: StatusAtleta | None = None,
        clube_id: UUID | None = None,
        somente_ativos: bool = True,
    ) -> list[Atleta]:
        if clube_id is not None:
            itens = await self.atleta_repo.list_by_clube(clube_id)
        elif modalidade is not None:
            itens = await self.atleta_repo.list_by_modalidade(modalidade)
        elif status is not None:
            itens = await self.atleta_repo.list_by_status(status)
        elif tipo is not None:
            itens = await self.atleta_repo.list_by_tipo(tipo)
        else:
            itens = await self.atleta_repo.list_all()
        if somente_ativos:
            return [item for item in itens if item.ativo]
        return itens

    async def atualizar_atleta(
        self,
        *,
        atleta_id: UUID,
        nome: str | None = None,
        tipo: TipoAtleta | None = None,
        modalidades: list[ModalidadeDesportiva] | None = None,
        posicoes: list[PosicaoAtleta] | None = None,
        pe_preferencial: PePreferencial | None = None,
        altura_cm: int | None = None,
        peso_kg: Decimal | None = None,
        clube_atual_id: UUID | None = None,
        numero_camisola: int | None = None,
        status: StatusAtleta | None = None,
        ultimo_exame_id: UUID | None = None,
        ativo: bool | None = None,
        observacoes: str | None = None,
    ) -> Atleta:
        item = await self.buscar_atleta(atleta_id)
        if ultimo_exame_id is not None and self.saude_service is not None:
            exame_ok = await self.saude_service.exame_exists(ultimo_exame_id)
            if not exame_ok:
                raise ValueError("Exame medico informado nao encontrado")
        item.atualizar(
            nome=nome,
            tipo=tipo,
            modalidades=modalidades,
            posicoes=posicoes,
            pe_preferencial=pe_preferencial,
            altura_cm=altura_cm,
            peso_kg=peso_kg,
            clube_atual_id=clube_atual_id,
            numero_camisola=numero_camisola,
            status=status,
            ultimo_exame_id=ultimo_exame_id,
            ativo=ativo,
            observacoes=observacoes,
        )
        return await self.atleta_repo.save(item)

    async def registrar_lesao(self, atleta_id: UUID) -> Atleta:
        item = await self.buscar_atleta(atleta_id)
        item.registrar_lesao()
        return await self.atleta_repo.save(item)

    async def recuperar_atleta(self, atleta_id: UUID) -> Atleta:
        item = await self.buscar_atleta(atleta_id)
        item.recuperar()
        return await self.atleta_repo.save(item)

    async def remover_atleta(self, atleta_id: UUID) -> None:
        deleted = await self.atleta_repo.delete(atleta_id)
        if not deleted:
            raise ValueError("Atleta nao encontrado")
