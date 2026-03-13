from __future__ import annotations
from datetime import date
from uuid import UUID
from apps.backend.app.modules.civil_protection.application.ports.bombeiro_repository_port import BombeiroRepositoryPort
from apps.backend.app.modules.civil_protection.application.ports.corporacao_repository_port import CorporacaoRepositoryPort
from apps.backend.app.modules.civil_protection.application.ports.request_service_port import RequestServicePort
from apps.backend.app.modules.civil_protection.domain.enums import CargoBombeiro, StatusAgenteProtecao
from apps.backend.app.modules.civil_protection.domain.models.bombeiro import Bombeiro

class BombeiroService:

    def __init__(self, *, bombeiro_repo: BombeiroRepositoryPort, corporacao_repo: CorporacaoRepositoryPort, request_service: RequestServicePort | None=None) -> None:
        self.bombeiro_repo = bombeiro_repo
        self.corporacao_repo = corporacao_repo
        self.request_service = request_service

    async def cadastrar_bombeiro(self, *, corporacao_id: UUID, nome: str, data_nascimento: date, cpf: str, rg: str, cargo: CargoBombeiro | None=None, telefone: str | None=None, email: str | None=None, endereco: str | None=None, observacoes: str | None=None, citizen_id: UUID | None=None) -> Bombeiro:
        corporacao = await self.corporacao_repo.get_by_id(corporacao_id)
        if corporacao is None:
            raise ValueError('Corporacao nao encontrada')
        existing = await self.bombeiro_repo.get_by_cpf(cpf)
        if existing is not None:
            raise ValueError('CPF ja cadastrado')
        matricula = await self.bombeiro_repo.next_matricula(corporacao_id)
        bombeiro = Bombeiro.cadastrar(matricula=matricula, corporacao_id=corporacao_id, nome=nome, data_nascimento=data_nascimento, cpf=cpf, rg=rg, cargo=cargo, telefone=telefone, email=email, endereco=endereco, observacoes=observacoes)
        saved = await self.bombeiro_repo.save(bombeiro)
        if self.request_service is not None:
            await self.request_service.create_request(request_type='CADASTRO_BOMBEIRO', entity_id=saved.id, citizen_id=citizen_id, numero_processo=saved.matricula, metadata={'matricula': saved.matricula, 'nome': saved.nome, 'corporacao': corporacao.nome})
        return saved

    async def buscar_bombeiro(self, bombeiro_id: UUID) -> Bombeiro:
        bombeiro = await self.bombeiro_repo.get_by_id(bombeiro_id)
        if bombeiro is None:
            raise ValueError('Bombeiro nao encontrado')
        return bombeiro

    async def listar_bombeiros(self, *, corporacao_id: UUID | None=None, status: StatusAgenteProtecao | None=None) -> list[Bombeiro]:
        if corporacao_id is not None:
            return await self.bombeiro_repo.list_by_corporacao(corporacao_id)
        if status is not None:
            return await self.bombeiro_repo.list_by_status(status)
        return await self.bombeiro_repo.list_all()

    async def atualizar_status(self, *, bombeiro_id: UUID, status: StatusAgenteProtecao, motivo: str | None=None) -> Bombeiro:
        bombeiro = await self.buscar_bombeiro(bombeiro_id)
        bombeiro.atualizar_status(status, motivo)
        return await self.bombeiro_repo.save(bombeiro)

    async def remover_bombeiro(self, bombeiro_id: UUID) -> None:
        deleted = await self.bombeiro_repo.delete(bombeiro_id)
        if not deleted:
            raise ValueError('Bombeiro nao encontrado')