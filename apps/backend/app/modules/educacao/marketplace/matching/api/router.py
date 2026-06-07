"""Router for Matching subdomain - FASE 3.2.2 IMPLEMENTATION"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.database.session import AsyncSessionLocal
from apps.backend.app.modules.educacao.infrastructure.models.institution_marketplace_projection_model import (
    InstitutionMarketplaceProjectionModel,
)
from foundation.matching import (
    CompatibilityCalculator,
    InstitutionProfile,
    MatchingEngine,
    MatchingScorer,
    RecommendationContext,
    RecommendationEngine,
    ResponseFormatter,
    StudentProfile,
)

from .health import matching_health

router = APIRouter(
    prefix="/marketplace/matching",
    tags=["marketplace", "matching"],
)

# Initialize matching components
matching_engine = MatchingEngine(
    scorer=MatchingScorer(),
    compatibility=CompatibilityCalculator(),
)
recommendation_engine = RecommendationEngine(matching_engine)
response_formatter = ResponseFormatter()


# Request/Response schemas
class StudentProfileRequest(BaseModel):
    """Request model for student profile"""

    student_id: str
    age: int
    academic_performance: float  # 0-100
    special_needs: list[str] = []
    location: dict[str, str]
    available_budget: float = 0.0
    preferred_modalities: list[str] = []
    educational_level: Optional[str] = None
    previous_transfers: int = 0


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/health", name="matching_health")
async def health_check():
    """Health check para Matching"""
    return await matching_health()


@router.post("/find-matches", name="find_matches")
async def find_matches(
    student: StudentProfileRequest,
    limit: int = Query(10, ge=1, le=50),
    session: AsyncSession = Depends(get_db),
):
    """Encontrar oportunidades compatíveis para cidadão - FASE 3.2.2

    Sistema de matching automático que recomenda as melhores escolas/cursos/vagas
    baseado no perfil do estudante.

    INPUT:
    {
        "student_id": "...",
        "age": 16,
        "academic_performance": 75.5,
        "special_needs": [],
        "location": {
            "province": "Luanda",
            "municipality": "Luanda",
            "district": "Maianga"
        },
        "available_budget": 30000,
        "preferred_modalities": ["presencial"],
        "educational_level": "secundario",
        "previous_transfers": 0
    }

    OUTPUT:
    [
        {
            "institution_id": "...",
            "match_score": 97,
            "reasons": [
                "vaga disponível",
                "compatível academicamente",
                "perto de casa"
            ]
        }
    ]

    Args:
        student: Perfil do estudante
        limit: Máximo de resultados
        session: Database session

    Returns:
        Lista de matches ordenados por compatibilidade
    """
    try:
        # Fetch all active institutions
        from sqlalchemy import select
        stmt = select(InstitutionMarketplaceProjectionModel).where(
            InstitutionMarketplaceProjectionModel.is_active == True
        )
        result = await session.execute(stmt)
        institution_models = result.scalars().all()

        # Convert to profiles
        student_profile = StudentProfile(
            student_id=student.student_id,
            age=student.age,
            academic_performance=student.academic_performance,
            special_needs=student.special_needs,
            location=student.location,
            available_budget=student.available_budget,
            preferred_modalities=student.preferred_modalities,
            educational_level=student.educational_level,
            previous_transfers=student.previous_transfers,
        )

        institution_profiles = []
        for inst_model in institution_models:
            profile = InstitutionProfile(
                institution_id=str(inst_model.institution_id),
                name=inst_model.name,
                type=inst_model.type,
                location={
                    "province": inst_model.province,
                    "municipality": inst_model.municipality,
                    "district": inst_model.district,
                },
                available_slots=inst_model.available_slots,
                monthly_fee=inst_model.monthly_fee_avg,
                rating=inst_model.rating,
                approval_rate=inst_model.approval_rate,
                academic_performance=inst_model.average_academic_performance,
                specializations=inst_model.specializations,
                supports_special_needs=inst_model.supports_special_needs,
                special_needs_types=inst_model.special_needs_types,
                teaching_modalities=inst_model.teaching_modalities,
                transfer_acceptance_rate=inst_model.transfer_acceptance_rate,
            )
            institution_profiles.append(profile)

        # Find matches
        matches = await matching_engine.find_matches(
            session=session,
            student=student_profile,
            institutions=institution_profiles,
            max_results=limit,
        )

        # Format response
        return {
            "student_id": student.student_id,
            "total": len(matches),
            "matches": response_formatter.format_match_results(matches),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no matching: {str(e)}")


@router.post("/eligibility/{student_id}/{institution_id}", name="check_eligibility")
async def check_eligibility(
    student_id: str,
    institution_id: str,
    student: StudentProfileRequest,
    session: AsyncSession = Depends(get_db),
):
    """Verificar elegibilidade do cidadão para oportunidade

    Args:
        student_id: ID do cidadão
        institution_id: ID da instituição
        student: Perfil do estudante
        session: Database session

    Returns:
        Resultado de elegibilidade com detalhes
    """
    try:
        # Fetch institution
        from sqlalchemy import select
        stmt = select(InstitutionMarketplaceProjectionModel).where(
            InstitutionMarketplaceProjectionModel.institution_id == institution_id
        )
        result = await session.execute(stmt)
        institution_model = result.scalar_one_or_none()

        if not institution_model:
            raise HTTPException(status_code=404, detail="Instituição não encontrada")

        # Convert to profiles
        student_profile = StudentProfile(
            student_id=student.student_id,
            age=student.age,
            academic_performance=student.academic_performance,
            special_needs=student.special_needs,
            location=student.location,
            available_budget=student.available_budget,
            preferred_modalities=student.preferred_modalities,
            educational_level=student.educational_level,
            previous_transfers=student.previous_transfers,
        )

        institution_profile = InstitutionProfile(
            institution_id=str(institution_model.institution_id),
            name=institution_model.name,
            type=institution_model.type,
            location={
                "province": institution_model.province,
                "municipality": institution_model.municipality,
                "district": institution_model.district,
            },
            available_slots=institution_model.available_slots,
            monthly_fee=institution_model.monthly_fee_avg,
            rating=institution_model.rating,
            approval_rate=institution_model.approval_rate,
            academic_performance=institution_model.average_academic_performance,
            specializations=institution_model.specializations,
            supports_special_needs=institution_model.supports_special_needs,
            special_needs_types=institution_model.special_needs_types,
            teaching_modalities=institution_model.teaching_modalities,
            transfer_acceptance_rate=institution_model.transfer_acceptance_rate,
        )

        # Check eligibility
        eligibility = await matching_engine.check_eligibility(
            session=session,
            student=student_profile,
            institution=institution_profile,
        )

        return {
            "student_id": student_id,
            "institution_id": institution_id,
            "institution_name": institution_model.name,
            **eligibility,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na verificação: {str(e)}")


@router.post("/recommendations", name="recommendations")
async def get_recommendations(
    student: StudentProfileRequest,
    limit: int = Query(5, ge=1, le=20),
    session: AsyncSession = Depends(get_db),
):
    """Gerar recomendações personalizadas para o estudante."""
    try:
        from sqlalchemy import select

        stmt = select(InstitutionMarketplaceProjectionModel).where(
            InstitutionMarketplaceProjectionModel.is_active == True
        )
        result = await session.execute(stmt)
        institution_models = result.scalars().all()

        student_profile = StudentProfile(
            student_id=student.student_id,
            age=student.age,
            academic_performance=student.academic_performance,
            special_needs=student.special_needs,
            location=student.location,
            available_budget=student.available_budget,
            preferred_modalities=student.preferred_modalities,
            educational_level=student.educational_level,
            previous_transfers=student.previous_transfers,
        )

        institution_profiles = []
        for inst_model in institution_models:
            institution_profiles.append(
                InstitutionProfile(
                    institution_id=str(inst_model.institution_id),
                    name=inst_model.name,
                    type=inst_model.type,
                    location={
                        "province": inst_model.province,
                        "municipality": inst_model.municipality,
                        "district": inst_model.district,
                    },
                    available_slots=inst_model.available_slots,
                    monthly_fee=inst_model.monthly_fee_avg,
                    rating=inst_model.rating,
                    approval_rate=inst_model.approval_rate,
                    academic_performance=inst_model.average_academic_performance,
                    specializations=inst_model.specializations,
                    supports_special_needs=inst_model.supports_special_needs,
                    special_needs_types=inst_model.special_needs_types,
                    teaching_modalities=inst_model.teaching_modalities,
                    transfer_acceptance_rate=inst_model.transfer_acceptance_rate,
                )
            )

        matches = await matching_engine.find_matches(
            session=session,
            student=student_profile,
            institutions=institution_profiles,
            max_results=limit,
        )

        recommendation = await recommendation_engine.generate_recommendation(
            RecommendationContext(
                student=student_profile,
                match_results=matches,
                institutions=institution_profiles,
            )
        )

        if not recommendation:
            return {
                "student_id": student.student_id,
                "total_matches": len(matches),
                "recommended_institution": None,
                "alternative_institutions": [],
                "reasoning": "Nenhuma recomendação disponível",
                "actions": [],
                "timeline": None,
                "success_probability": 0.0,
            }

        return {
            "student_id": student.student_id,
            "total_matches": len(matches),
            "recommended_institution": response_formatter.format_match_result(
                recommendation.primary_match
            ),
            "alternative_institutions": response_formatter.format_match_results(
                recommendation.alternative_matches
            ),
            "reasoning": recommendation.reasoning,
            "actions": recommendation.suggested_actions,
            "timeline": recommendation.timeline,
            "success_probability": round(recommendation.success_probability, 2),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na recomendação: {str(e)}")


@router.get("/recommendations/{student_id}", name="get_recommendations")
async def get_recommendations(
    student_id: str,
    student: StudentProfileRequest,
    limit: int = Query(5, ge=1, le=20),
    session: AsyncSession = Depends(get_db),
):
    """Obter recomendações personalizadas para estudante

    Args:
        student_id: ID do cidadão
        student: Perfil do estudante
        limit: Máximo de recomendações
        session: Database session

    Returns:
        Recomendações personalizadas
    """
    try:
        # Get matches
        from sqlalchemy import select
        stmt = select(InstitutionMarketplaceProjectionModel).where(
            InstitutionMarketplaceProjectionModel.is_active == True
        )
        result = await session.execute(stmt)
        institution_models = result.scalars().all()

        # Convert to profiles
        student_profile = StudentProfile(
            student_id=student.student_id,
            age=student.age,
            academic_performance=student.academic_performance,
            special_needs=student.special_needs,
            location=student.location,
            available_budget=student.available_budget,
            preferred_modalities=student.preferred_modalities,
            educational_level=student.educational_level,
            previous_transfers=student.previous_transfers,
        )

        institution_profiles = []
        for inst_model in institution_models:
            profile = InstitutionProfile(
                institution_id=str(inst_model.institution_id),
                name=inst_model.name,
                type=inst_model.type,
                location={
                    "province": inst_model.province,
                    "municipality": inst_model.municipality,
                    "district": inst_model.district,
                },
                available_slots=inst_model.available_slots,
                monthly_fee=inst_model.monthly_fee_avg,
                rating=inst_model.rating,
                approval_rate=inst_model.approval_rate,
                academic_performance=inst_model.average_academic_performance,
                specializations=inst_model.specializations,
                supports_special_needs=inst_model.supports_special_needs,
                special_needs_types=inst_model.special_needs_types,
                teaching_modalities=inst_model.teaching_modalities,
                transfer_acceptance_rate=inst_model.transfer_acceptance_rate,
            )
            institution_profiles.append(profile)

        # Get matches
        matches = await matching_engine.find_matches(
            session=session,
            student=student_profile,
            institutions=institution_profiles,
            max_results=limit,
        )

        return {
            "student_id": student_id,
            "total": len(matches),
            "recommendations": response_formatter.format_match_results(matches),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro nas recomendações: {str(e)}")
