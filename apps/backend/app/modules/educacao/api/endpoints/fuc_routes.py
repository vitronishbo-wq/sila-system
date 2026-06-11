from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_current_user, get_db
from apps.backend.app.modules.educacao.infrastructure.models.matricula_model import MatriculaModel
from apps.backend.app.modules.educacao.infrastructure.models.boletim_model import BoletimModel
from apps.backend.app.modules.educacao.infrastructure.models.certificado_model import CertificadoModel
from apps.backend.app.modules.educacao.infrastructure.models.academic_identity_model import AcademicIdentityModel
from apps.backend.app.modules.educacao.infrastructure.models.enrollment_model import EnrollmentModel
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel

router = APIRouter(prefix="/fuc", tags=["Educacao - FUC"])


@router.get("/{citizen_id}/educacao")
async def fuc_educacao(
    citizen_id: UUID,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    matriculas = (
        (await session.execute(
            select(MatriculaModel).where(MatriculaModel.citizen_id == citizen_id)
        ))
        .scalars()
        .all()
    )
    boletins = (
        (await session.execute(
            select(BoletimModel).where(BoletimModel.citizen_id == citizen_id)
        ))
        .scalars()
        .all()
    )
    certificados = (
        (await session.execute(
            select(CertificadoModel).where(CertificadoModel.citizen_id == citizen_id)
        ))
        .scalars()
        .all()
    )
    identities = (
        (await session.execute(
            select(AcademicIdentityModel).where(AcademicIdentityModel.id == citizen_id)
        ))
        .scalars()
        .all()
    )
    enrollments = []
    for identity in identities:
        rows = (
            await session.execute(
                select(EnrollmentModel).where(EnrollmentModel.student_id == identity.id)
            )
        ).scalars().all()
        enrollments.extend(rows)

    async def _escola_nome(escola_id):
        escola = await session.get(EscolaModel, escola_id)
        return escola.nome if escola else "Desconhecida"

    return {
        "identidades": [
            {
                "id": str(i.id),
                "nome": i.full_name,
                "ns_number": i.national_student_number,
                "status": i.academic_status,
            }
            for i in identities
        ],
        "matriculas": [
            {
                "id": str(m.id),
                "numero_processo": m.numero_processo,
                "escola_nome": await _escola_nome(m.escola_id),
                "data": str(m.data_matricula),
                "status": m.status,
            }
            for m in matriculas
        ],
        "enrollments": [
            {
                "id": str(e.id),
                "institution_id": str(e.institution_id),
                "academic_year": e.academic_year,
                "grade": e.grade,
                "status": e.status,
            }
            for e in enrollments
        ],
        "boletins": [
            {
                "id": str(b.id),
                "numero_processo": b.numero_processo,
                "data": str(b.data_registo),
                "status": b.status,
            }
            for b in boletins
        ],
        "certificados": [
            {
                "id": str(c.id),
                "numero_processo": c.numero_processo,
                "data": str(c.data_registo),
                "status": c.status,
            }
            for c in certificados
        ],
    }
