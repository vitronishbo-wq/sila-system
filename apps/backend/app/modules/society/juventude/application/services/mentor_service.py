from __future__ import annotations
from uuid import UUID
from app.modules.society.juventude.application.ports.mentor_repository_port import MentorRepositoryPort
from app.modules.society.juventude.domain.enums import AreaInteresse, StatusMentoria, TipoMentoria
from app.modules.society.juventude.domain.models.mentor import Mentor

class MentorService:

    def __init__(self, *, mentor_repo: MentorRepositoryPort) -> None:
        self.mentor_repo = mentor_repo

    async def cadastrar_mentor(self, *, nome: str, tipo_mentoria: TipoMentoria, area_interesse: AreaInteresse, email: str | None=None, telefone: str | None=None, observacoes: str | None=None) -> Mentor:
        codigo = await self.mentor_repo.next_codigo()
        item = Mentor.cadastrar(codigo_mentor=codigo, nome=nome, tipo_mentoria=tipo_mentoria, area_interesse=area_interesse, email=email, telefone=telefone, observacoes=observacoes)
        return await self.mentor_repo.save(item)

    async def buscar_mentor(self, mentor_id: UUID) -> Mentor:
        item = await self.mentor_repo.get_by_id(mentor_id)
        if item is None:
            raise ValueError('Mentor nao encontrado')
        return item

    async def listar_mentores(self, *, status: StatusMentoria | None=None) -> list[Mentor]:
        if status is not None:
            return await self.mentor_repo.list_by_status(status)
        return await self.mentor_repo.list_all()

    async def atribuir_jovem(self, *, mentor_id: UUID, jovem_id: UUID) -> Mentor:
        mentor = await self.buscar_mentor(mentor_id)
        mentor.atribuir_jovem(jovem_id)
        return await self.mentor_repo.save(mentor)

    async def atualizar_status(self, *, mentor_id: UUID, status: StatusMentoria) -> Mentor:
        mentor = await self.buscar_mentor(mentor_id)
        mentor.atualizar_status(status)
        return await self.mentor_repo.save(mentor)

    async def remover_mentor(self, mentor_id: UUID) -> None:
        if not await self.mentor_repo.delete(mentor_id):
            raise ValueError('Mentor nao encontrado')