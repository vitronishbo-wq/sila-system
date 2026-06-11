from __future__ import annotations

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.api.deps import get_current_user
from apps.backend.app.core.database.session import AsyncSessionLocal
from apps.backend.app.modules.educacao.api.schemas.marketplace_schema import (
    RecomendacaoResult,
    SchoolCard,
    SchoolSearchResult,
    SeatReservationCreate,
    SeatReservationResponse,
    VacancyResult,
    VacancySearchResult,
)
from apps.backend.app.modules.educacao.application.marketplace.marketplace_service import (
    CapacityService,
    MatchingService,
    SeatReservationService,
    StudentProfile,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.marketplace_institution_repository import (
    MarketplaceInstitutionRepository,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.marketplace_vacancy_repository import (
    MarketplaceVacancyRepository,
)
from apps.backend.app.modules.educacao.infrastructure.repositories.seat_reservation_repository import (
    SeatReservationRepository,
)
from apps.backend.app.modules.educacao.infrastructure.models.escola_model import EscolaModel
from apps.backend.app.core.rbac.territorial_access import verify_territorial_access
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/marketplace",
    tags=["Educacao - Marketplace"],
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/escolas", response_model=SchoolSearchResult)
async def buscar_escolas(
    provincia: Optional[str] = Query(None, max_length=128),
    municipio: Optional[str] = Query(None, max_length=128),
    bairro: Optional[str] = Query(None, max_length=128),
    tipo: Optional[str] = Query(None, pattern=r"^(publica|privada|comunitaria)$"),
    nivel_ensino: Optional[str] = Query(None, max_length=64),
    q: Optional[str] = Query(None, max_length=255, description="Pesquisa por nome"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    repo = MarketplaceInstitutionRepository(session)
    items, total = await repo.search(
        provincia=provincia,
        municipio=municipio,
        bairro=bairro,
        tipo=tipo,
        nivel_ensino=nivel_ensino,
        q=q,
        page=page,
        page_size=page_size,
    )
    return SchoolSearchResult(
        total=total,
        page=page,
        page_size=page_size,
        results=[
            SchoolCard(
                institution_id=inst.institution_id,
                nome=inst.nome,
                tipo=inst.tipo,
                nivel_ensino=inst.nivel_ensino,
                provincia=inst.provincia,
                municipio=inst.municipio,
                bairro=inst.bairro,
                latitude=inst.latitude,
                longitude=inst.longitude,
                turnos=inst.turnos.split(","),
                contactos=inst.contactos,
                status=inst.status,
            )
            for inst in items
        ],
    )


@router.get("/escolas/{institution_id}", response_model=SchoolCard)
async def obter_escola(
    institution_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    repo = MarketplaceInstitutionRepository(session)
    inst = await repo.get_by_institution_id(institution_id)
    if not inst:
        raise HTTPException(status_code=404, detail="Escola nao encontrada")
    return SchoolCard(
        institution_id=inst.institution_id,
        nome=inst.nome,
        tipo=inst.tipo,
        nivel_ensino=inst.nivel_ensino,
        provincia=inst.provincia,
        municipio=inst.municipio,
        bairro=inst.bairro,
        latitude=inst.latitude,
        longitude=inst.longitude,
        turnos=inst.turnos.split(","),
        contactos=inst.contactos,
        status=inst.status,
    )


@router.get("/vagas", response_model=VacancySearchResult)
async def buscar_vagas(
    provincia: Optional[str] = Query(None, max_length=128),
    municipio: Optional[str] = Query(None, max_length=128),
    classe: Optional[str] = Query(None, max_length=32),
    turno: Optional[str] = Query(None, pattern=r"^(manha|tarde|noite|integral)$"),
    instituicao_id: Optional[uuid.UUID] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    vacancy_repo = MarketplaceVacancyRepository(session)
    inst_repo = MarketplaceInstitutionRepository(session)
    items, total = await vacancy_repo.search(
        provincia=provincia,
        municipio=municipio,
        classe=classe,
        turno=turno,
        instituicao_id=instituicao_id,
        page=page,
        page_size=page_size,
    )
    results = []
    for item in items:
        inst = await inst_repo.get_by_institution_id(item.institution_id)
        results.append(VacancyResult(
            institution_id=item.institution_id,
            nome_escola=inst.nome if inst else "Desconhecida",
            ano_letivo=item.ano_letivo,
            classe=item.classe,
            turno=item.turno,
            vagas_disponiveis=item.vagas_disponiveis,
            vagas_totais=item.vagas_totais,
        ))
    return VacancySearchResult(total=total, page=page, page_size=page_size, results=results)


@router.get("/recomendacoes", response_model=list[dict])
async def recomendar_escolas(
    provincia: str = Query(..., max_length=128),
    municipio: str = Query(..., max_length=128),
    bairro: Optional[str] = Query(None, max_length=128),
    classe: Optional[str] = Query(None, max_length=32),
    nivel_ensino: Optional[str] = Query(None, max_length=64),
    turno: Optional[str] = Query(None, max_length=32),
    ano_letivo: str = Query(..., max_length=32),
    limit: int = Query(10, ge=1, le=50),
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    inst_repo = MarketplaceInstitutionRepository(session)
    vacancy_repo = MarketplaceVacancyRepository(session)
    service = MatchingService(inst_repo, vacancy_repo)
    profile = StudentProfile(
        student_id=uuid.uuid4(),
        provincia=provincia,
        municipio=municipio,
        bairro=bairro,
        classe=classe,
        nivel_ensino=nivel_ensino,
        turno_preferido=turno,
    )
    matches = await service.find_matches(profile, ano_letivo, limit=limit)
    return [
        {
            "escola": m["nome"],
            "score": m["score"],
            "motivos": m["motivos"],
            "nivel_ensino": m["nivel_ensino"],
            "provincia": m["provincia"],
            "municipio": m["municipio"],
        }
        for m in matches
    ]


@router.post("/reservar", response_model=dict)
async def reservar_vaga(
    data: SeatReservationCreate,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    vacancy_repo = MarketplaceVacancyRepository(session)
    reservation_repo = SeatReservationRepository(session)
    service = SeatReservationService(reservation_repo, vacancy_repo)
    # territorial check: ensure user can act on the target institution territory
    escola_model = await session.get(EscolaModel, data.institution_id)
    if not escola_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instituicao nao encontrada")
    await verify_territorial_access(user=user, resource_territory_id=getattr(escola_model, "territory_id", None), db=session)

    result = await service.create_reservation(
        student_id=data.student_id,
        institution_id=data.institution_id,
        classe=data.classe,
        turno=data.turno,
        ano_letivo=data.ano_letivo,
    )
    if not result.get("criada"):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=result.get("erro", "Falha na reserva"))
    return result


@router.get("/reservas/{student_id}", response_model=list[dict])
async def listar_reservas(
    student_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    reservation_repo = SeatReservationRepository(session)
    service = SeatReservationService(reservation_repo, MarketplaceVacancyRepository(session))
    return await service.list_active(student_id)


@router.post("/reservas/{reservation_id}/confirmar", response_model=dict)
async def confirmar_reserva(
    reservation_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
    idempotency_key: str | None = None,
):
    reservation_repo = SeatReservationRepository(session)
    vacancy_repo = MarketplaceVacancyRepository(session)
    service = SeatReservationService(reservation_repo, vacancy_repo)
    # territorial check: ensure user can act on the reservation's institution
    reservation = await reservation_repo.get_by_id(reservation_id)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva nao encontrada")
    escola_model = await session.get(EscolaModel, reservation.institution_id)
    await verify_territorial_access(user=user, resource_territory_id=getattr(escola_model, "territory_id", None), db=session)

    ok = await service.confirm_reservation(reservation_id, request_id=str(_idempotency_or_request_id(idempotency_key)))
    if not ok:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nao foi possivel confirmar a reserva")
    await session.commit()
    return {"status": "confirmed", "reservation_id": str(reservation_id)}


@router.post("/reservas/{reservation_id}/cancelar", response_model=dict)
async def cancelar_reserva(
    reservation_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    reservation_repo = SeatReservationRepository(session)
    vacancy_repo = MarketplaceVacancyRepository(session)
    service = SeatReservationService(reservation_repo, vacancy_repo)
    # territorial check: ensure user can act on the reservation's institution
    reservation = await reservation_repo.get_by_id(reservation_id)
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva nao encontrada")
    escola_model = await session.get(EscolaModel, reservation.institution_id)
    await verify_territorial_access(user=user, resource_territory_id=getattr(escola_model, "territory_id", None), db=session)

    ok = await service.cancel_reservation(reservation_id, request_id=str(_idempotency_or_request_id(None)))
    if not ok:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nao foi possivel cancelar a reserva")
    await session.commit()
    return {"status": "cancelled", "reservation_id": str(reservation_id)}


def _idempotency_or_request_id(key: str | None) -> str:
    if key:
        return key
    import uuid
    return str(uuid.uuid4())
