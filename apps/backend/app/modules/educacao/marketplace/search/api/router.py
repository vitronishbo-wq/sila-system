"""Router for Search subdomain - FASE 3.2.1 IMPLEMENTATION"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.app.core.database.session import AsyncSessionLocal
from apps.backend.app.modules.educacao.infrastructure.models.institution_marketplace_projection_model import (
    InstitutionMarketplaceProjectionModel,
)
from foundation.search import SearchEngine, SearchQuery

from .health import search_health

router = APIRouter(
    prefix="/search",
    tags=["marketplace", "search"],
)

# Initialize search engine
search_engine = SearchEngine()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/health", name="search_health")
async def health_check() -> dict[str, str]:
    """Health check para Search"""
    return await search_health()


@router.get("/", name="marketplace_search")
async def marketplace_search(
    q: Optional[str] = Query(None, description="Texto de busca"),
    city: Optional[str] = Query(None, description="Cidade"),
    district: Optional[str] = Query(None, description="Bairro"),
    educational_level: Optional[str] = Query(None, description="Nível educacional"),
    age: Optional[int] = Query(None, description="Idade do estudante"),
    price_min: Optional[float] = Query(None, description="Propina mínima"),
    price_max: Optional[float] = Query(None, description="Propina máxima"),
    modality: Optional[str] = Query(None, description="Modalidade (presencial, remoto, hibrido)"),
    institution_type: Optional[str] = Query(None, description="Tipo de instituição"),
    min_slots: Optional[int] = Query(None, description="Mínimo de vagas"),
    has_special_needs_support: Optional[bool] = Query(None, description="Suporta necessidades especiais"),
    min_rating: Optional[float] = Query(None, description="Classificação mínima"),
    sort_by: Optional[str] = Query(
        None,
        description="Ordenar por: relevance, price, rating, quality, slots, distance, featured",
    ),
    page: int = Query(1, ge=1, description="Página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
    session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
    """Busca avançada no Marketplace Educacional - GET /educacao/marketplace/search

    Filtros Disponíveis:
    - q: Texto de busca livre
    - city: Cidade
    - district: Bairro
    - educational_level: Nível (primario, secundario, superior)
    - age: Idade do estudante
    - price_min/price_max: Range de propina
    - modality: Modalidade (presencial, remoto, hibrido)
    - institution_type: Tipo (publica, privada, comunitaria)
    - min_slots: Mínimo de vagas disponíveis
    - has_special_needs_support: Suporta necessidades especiais
    - min_rating: Classificação mínima (0-5)
    - page: Número da página
    - page_size: Itens por página (1-100)

    Returns:
        Resultados de busca paginados com ranking por relevância
    """
    try:
        sort_map = {
            "price": ("monthly_fee_avg", "asc"),
            "rating": ("rating", "desc"),
            "quality": ("quality_index", "desc"),
            "slots": ("available_slots", "desc"),
            "distance": ("default_distance_score", "desc"),
            "featured": ("is_featured", "desc"),
        }

        sort_field = None
        sort_order = "desc"
        if sort_by:
            mapped = sort_map.get(sort_by.lower())
            if mapped:
                sort_field, sort_order = mapped

        search_query = SearchQuery(
            text=q,
            page=page,
            page_size=page_size,
            sort_by=sort_field,
            sort_order=sort_order,
        )

        filters = {}

        if city:
            filters[InstitutionMarketplaceProjectionModel.municipality] = city

        if district:
            filters[InstitutionMarketplaceProjectionModel.district] = district

        if institution_type:
            filters[InstitutionMarketplaceProjectionModel.type] = institution_type

        if modality:
            filters[InstitutionMarketplaceProjectionModel.teaching_modalities] = {"in": [modality]}

        if educational_level:
            filters[InstitutionMarketplaceProjectionModel.educational_levels] = {"in": [educational_level]}

        if min_slots is not None:
            filters[InstitutionMarketplaceProjectionModel.available_slots] = {"gte": min_slots}

        if price_min is not None or price_max is not None:
            price_filter = {}
            if price_min is not None:
                price_filter["gte"] = price_min
            if price_max is not None:
                price_filter["lte"] = price_max
            filters[InstitutionMarketplaceProjectionModel.monthly_fee_avg] = price_filter

        if has_special_needs_support:
            filters[InstitutionMarketplaceProjectionModel.supports_special_needs] = True

        if min_rating is not None:
            filters[InstitutionMarketplaceProjectionModel.rating] = {"gte": min_rating}

        filters[InstitutionMarketplaceProjectionModel.is_active] = True

        search_fields = [
            InstitutionMarketplaceProjectionModel.name,
            InstitutionMarketplaceProjectionModel.description,
            InstitutionMarketplaceProjectionModel.specializations,
        ]

        result = await search_engine.search(
            session=session,
            model=InstitutionMarketplaceProjectionModel,
            query=search_query,
            search_fields=search_fields,
            filters=filters,
        )

        institutions = []
        for item in result.items:
            institutions.append({
                "id": str(item.institution_id),
                "name": item.name,
                "type": item.type,
                "city": item.municipality,
                "district": item.district,
                "rating": item.rating,
                "review_count": item.review_count,
                "available_slots": item.available_slots,
                "monthly_fee_min": item.monthly_fee_min,
                "monthly_fee_max": item.monthly_fee_max,
                "monthly_fee_avg": item.monthly_fee_avg,
                "quality_index": getattr(item, "quality_index", 0.0),
                "distance_score": getattr(item, "default_distance_score", 0.0),
                "approval_rate": item.approval_rate,
                "transfer_acceptance_rate": item.transfer_acceptance_rate,
                "modalities": item.teaching_modalities,
                "levels": item.educational_levels,
                "specializations": item.specializations,
                "supports_special_needs": item.supports_special_needs,
                "accreditation": item.accreditation_status,
                "featured": item.is_featured,
            })

        return {
            "query": q or "",
            "sort_by": sort_by or "relevance",
            "filters_applied": {
                "city": city,
                "district": district,
                "educational_level": educational_level,
                "modality": modality,
                "type": institution_type,
                "price_range": [price_min, price_max] if price_min or price_max else None,
                "min_slots": min_slots,
                "min_rating": min_rating,
                "special_needs": has_special_needs_support,
            },
            "total": result.total if result.total is not None else len(institutions),
            "page": page,
            "page_size": page_size,
            "results": institutions,
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Erro na busca",
            "results": [],
        }


@router.post("/advanced", name="advanced_search")
async def advanced_search(
    query: str,
    level: Optional[str] = None,
    institution: Optional[str] = None,
    modality: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    sort_by: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
    """Busca avançada com múltiplos filtros (legacy endpoint)

    Args:
        query: String de busca
        level: Nível educacional
        institution: Instituição
        modality: Modalidade (presencial, remoto, híbrido)
        price_min: Preço mínimo
        price_max: Preço máximo
        page: Página
        page_size: Tamanho da página
        
    Returns:
        Resultados de busca
    """
    return await marketplace_search(
        q=query,
        educational_level=level,
        institution_type=institution,
        modality=modality,
        price_min=price_min,
        price_max=price_max,
        sort_by=sort_by,
        page=page,
        page_size=page_size,
        session=session,
    )


@router.get("/nearby", name="search_nearby")
async def search_nearby(
    latitude: float,
    longitude: float,
    radius_km: float = 10,
    page: int = Query(1, ge=1, description="Página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
    session: AsyncSession = Depends(get_db),
) -> dict[str, object]:
    """Busca de oportunidades próximas usando heurística de distância disponível.

    Args:
        latitude: Latitude
        longitude: Longitude
        radius_km: Raio de busca em km
        page: página de resultados
        page_size: itens por página

    Returns:
        Oportunidades ordenadas por score de proximidade
    """
    from sqlalchemy import select

    # Current projection model does not hold exact geocoordinates,
    # so we rely on the precomputed distance score as a proxy for proximity.
    stmt = (
        select(InstitutionMarketplaceProjectionModel)
        .where(InstitutionMarketplaceProjectionModel.is_active == True)
        .order_by(InstitutionMarketplaceProjectionModel.default_distance_score.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    result = await session.execute(stmt)
    items = result.scalars().all()

    opportunities = []
    for item in items:
        opportunities.append(
            {
                "id": str(item.institution_id),
                "name": item.name,
                "city": item.municipality,
                "district": item.district,
                "distance_score": getattr(item, "default_distance_score", 0.0),
                "available_slots": item.available_slots,
                "monthly_fee_avg": item.monthly_fee_avg,
                "rating": item.rating,
            }
        )

    return {
        "latitude": latitude,
        "longitude": longitude,
        "radius_km": radius_km,
        "page": page,
        "page_size": page_size,
        "opportunities": opportunities,
        "message": "Resultados ordenados por score de proximidade disponível",
    }
