from uuid import UUID

from apps.backend.app.modules.educacao.application.ports.guardian_repository_port import GuardianRepositoryPort
from apps.backend.app.modules.educacao.domain.academic_identity import GuardianRelationship
from apps.backend.app.modules.educacao.infrastructure.models.guardian_model import GuardianModel
from apps.backend.app.modules.educacao.infrastructure.models.guardian_student_link import GuardianStudentLink


class EncarregadosService:
    def __init__(self, repo: GuardianRepositoryPort, session=None):
        self._repo = repo
        self._session = session

    async def registar_encarregado(
        self, full_name: str, relationship: str, document_id: str | None = None,
        phone: str | None = None, email: str | None = None,
        address: str | None = None, province: str | None = None,
        municipio: str | None = None,
    ) -> GuardianModel:
        guardian = GuardianModel(
            full_name=full_name,
            relationship=relationship,
            document_id=document_id,
            phone=phone,
            email=email,
            address=address,
            province=province,
            municipio=municipio,
        )
        return await self._repo.create(guardian)

    async def associar_estudante(self, guardian_id: UUID, student_id: UUID, relationship: str) -> None:
        await self._repo.link_to_student(guardian_id, student_id, relationship)

    async def consultar_encarregado(self, guardian_id: UUID) -> GuardianModel | None:
        return await self._repo.get_by_id(guardian_id)

    async def listar_encarregados_do_estudante(self, student_id: UUID) -> list[GuardianModel]:
        return await self._repo.find_by_student(student_id)

    async def buscar_por_documento(self, document_id: str) -> list[GuardianModel]:
        return await self._repo.find_by_document(document_id)

    async def atualizar_encarregado(self, guardian: GuardianModel) -> GuardianModel:
        return await self._repo.update(guardian)
