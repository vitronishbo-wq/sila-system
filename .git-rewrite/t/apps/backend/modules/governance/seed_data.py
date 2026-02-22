"""
Seed data script for Governance module.

This script populates the governance tables with initial data:
- Institutions (government institutions)
- Mandates (linked to institutions)
- Council Meetings
- Decisions (linked to council meetings)

Run this after migrations to have governance data available for testing.
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone
from uuid import UUID

# Add backend to path
sys.path.insert(0, sys.path[0] + "/.." if sys.path[0] else "..")

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import AsyncSessionLocal
from modules.governance.models import (
    CouncilMeeting,
    Decision,
    Institution,
    Mandate,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Fixed UUIDs for consistent relationships
# These UUIDs are deterministic to ensure relationships work correctly
INSTITUTION_MINSA = UUID("11111111-1111-1111-1111-111111111111")
INSTITUTION_MED = UUID("22222222-2222-2222-2222-222222222222")
INSTITUTION_MPD = UUID("33333333-3333-3333-3333-333333333333")
INSTITUTION_MPT = UUID("44444444-4444-4444-4444-444444444444")

COUNCIL_MEETING_1 = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
COUNCIL_MEETING_2 = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")

# Default institutions data
DEFAULT_INSTITUTIONS = [
    {
        "id": INSTITUTION_MINSA,
        "name": "Ministério da Saúde",
        "acronym": "MINSA",
        "institution_type": "ministry",
        "jurisdiction": "Angola",
        "description": "Ministério responsável pelas políticas de saúde pública em Angola",
        "founding_date": datetime(1975, 11, 11, tzinfo=timezone.utc),
        "website": "https://www.minsa.gov.ao",
        "contact_info": {
            "email": "info@minsa.gov.ao",
            "phone": "+244 222 123 456",
            "address": "Luanda, Angola",
        },
        "leadership": {
            "minister": "Dr. Sílvia Lutucuta",
            "deputy_ministers": ["Dr. José Vieira Dias", "Dr. Leonardo Inocêncio"],
        },
        "parent_institution_id": None,
    },
    {
        "id": INSTITUTION_MED,
        "name": "Ministério da Educação",
        "acronym": "MED",
        "institution_type": "ministry",
        "jurisdiction": "Angola",
        "description": "Ministério responsável pelas políticas educacionais em Angola",
        "founding_date": datetime(1975, 11, 11, tzinfo=timezone.utc),
        "website": "https://www.med.gov.ao",
        "contact_info": {
            "email": "info@med.gov.ao",
            "phone": "+244 222 234 567",
            "address": "Luanda, Angola",
        },
        "leadership": {
            "minister": "Luísa Grilo",
            "deputy_ministers": ["Ana Paula Tuavanje", "Francisco Manuel"],
        },
        "parent_institution_id": None,
    },
    {
        "id": INSTITUTION_MPD,
        "name": "Ministério da Defesa",
        "acronym": "MPD",
        "institution_type": "ministry",
        "jurisdiction": "Angola",
        "description": "Ministério responsável pela defesa nacional",
        "founding_date": datetime(1975, 11, 11, tzinfo=timezone.utc),
        "website": "https://www.mpd.gov.ao",
        "contact_info": {
            "email": "info@mpd.gov.ao",
            "phone": "+244 222 345 678",
            "address": "Luanda, Angola",
        },
        "leadership": {
            "minister": "João Ernesto dos Santos",
            "deputy_ministers": ["General António", "General Manuel"],
        },
        "parent_institution_id": None,
    },
    {
        "id": INSTITUTION_MPT,
        "name": "Ministério das Obras Públicas e Urbanismo",
        "acronym": "MPT",
        "institution_type": "ministry",
        "jurisdiction": "Angola",
        "description": "Ministério responsável por obras públicas e desenvolvimento urbano",
        "founding_date": datetime(1975, 11, 11, tzinfo=timezone.utc),
        "website": "https://www.mpt.gov.ao",
        "contact_info": {
            "email": "info@mpt.gov.ao",
            "phone": "+244 222 456 789",
            "address": "Luanda, Angola",
        },
        "leadership": {
            "minister": "Manuel Tavares de Almeida",
            "deputy_ministers": ["Eng. Carlos", "Eng. Maria"],
        },
        "parent_institution_id": None,
    },
]

# Default mandates data (linked to institutions)
DEFAULT_MANDATES = [
    {
        "title": "Mandato de Gestão da Saúde Pública 2024-2028",
        "description": "Mandato para gestão e coordenação das políticas de saúde pública",
        "mandate_type": "executive",
        "issuing_authority": "Presidência da República",
        "start_date": datetime(2024, 1, 1, tzinfo=timezone.utc),
        "end_date": datetime(2028, 12, 31, tzinfo=timezone.utc),
        "status": "active",
        "scope": {
            "geographic": "Nacional",
            "areas": ["Saúde pública", "Prevenção de doenças", "Gestão hospitalar"],
        },
        "related_documents": {
            "decree": "Decreto Presidencial 123/2024",
            "law": "Lei 45/2023",
        },
        "institution_id": INSTITUTION_MINSA,
    },
    {
        "title": "Mandato de Reforma Educacional 2024-2028",
        "description": "Mandato para implementação de reformas no sistema educacional",
        "mandate_type": "executive",
        "issuing_authority": "Presidência da República",
        "start_date": datetime(2024, 1, 1, tzinfo=timezone.utc),
        "end_date": datetime(2028, 12, 31, tzinfo=timezone.utc),
        "status": "active",
        "scope": {
            "geographic": "Nacional",
            "areas": ["Educação básica", "Ensino superior", "Formação profissional"],
        },
        "related_documents": {
            "decree": "Decreto Presidencial 124/2024",
            "law": "Lei 46/2023",
        },
        "institution_id": INSTITUTION_MED,
    },
    {
        "title": "Mandato de Modernização das Forças Armadas 2023-2027",
        "description": "Mandato para modernização e capacitação das forças armadas",
        "mandate_type": "executive",
        "issuing_authority": "Presidência da República",
        "start_date": datetime(2023, 1, 1, tzinfo=timezone.utc),
        "end_date": datetime(2027, 12, 31, tzinfo=timezone.utc),
        "status": "active",
        "scope": {
            "geographic": "Nacional",
            "areas": ["Defesa nacional", "Modernização tecnológica", "Treinamento"],
        },
        "related_documents": {
            "decree": "Decreto Presidencial 100/2023",
            "law": "Lei 40/2022",
        },
        "institution_id": INSTITUTION_MPD,
    },
]

# Default council meetings data
DEFAULT_COUNCIL_MEETINGS = [
    {
        "id": COUNCIL_MEETING_1,
        "title": "Reunião Ordinária do Conselho de Ministros - Janeiro 2025",
        "description": "Reunião mensal para discussão de políticas públicas e aprovação de decisões",
        "location": "Palácio Presidencial, Luanda",
        "start_time": datetime(2025, 1, 15, 9, 0, tzinfo=timezone.utc),
        "end_time": datetime(2025, 1, 15, 13, 0, tzinfo=timezone.utc),
        "status": "completed",
        "agenda": {
            "items": [
                "Aprovação do orçamento 2025",
                "Discussão sobre políticas de saúde",
                "Revisão de projetos de infraestrutura",
            ]
        },
        "minutes": {
            "summary": "Reunião produtiva com aprovação de várias decisões importantes",
            "attendees": ["Presidente", "Vice-Presidente", "Ministros"],
            "key_points": ["Orçamento aprovado", "Políticas de saúde discutidas"],
        },
        "decisions": {"count": 3, "approved": 3},
        "participants": {
            "president": "Presidente da República",
            "ministers": ["MINSA", "MED", "MPD", "MPT"],
            "total": 25,
        },
        "council_id": None,
    },
    {
        "id": COUNCIL_MEETING_2,
        "title": "Reunião Extraordinária - Emergência de Saúde",
        "description": "Reunião de emergência para discutir medidas de saúde pública",
        "location": "Palácio Presidencial, Luanda",
        "start_time": datetime(2025, 2, 1, 10, 0, tzinfo=timezone.utc),
        "end_time": datetime(2025, 2, 1, 12, 0, tzinfo=timezone.utc),
        "status": "scheduled",
        "agenda": {
            "items": [
                "Situação epidemiológica",
                "Medidas preventivas",
                "Alocação de recursos",
            ]
        },
        "minutes": None,
        "decisions": None,
        "participants": {
            "president": "Presidente da República",
            "ministers": ["MINSA", "MPD"],
            "total": 15,
        },
        "council_id": None,
    },
]

# Default decisions data (linked to council meetings)
DEFAULT_DECISIONS = [
    {
        "title": "Aprovação do Orçamento Geral do Estado 2025",
        "description": "Aprovação do orçamento anual para o exercício fiscal de 2025",
        "decision_type": "policy",
        "status": "approved",
        "voting_record": {
            "votes_for": 20,
            "votes_against": 2,
            "abstentions": 3,
            "quorum": 0.83,
        },
        "meeting_id": COUNCIL_MEETING_1,
        "effective_date": datetime(2025, 1, 16, tzinfo=timezone.utc),
        "expiration_date": datetime(2025, 12, 31, tzinfo=timezone.utc),
        "related_documents": {
            "law": "Lei Orçamental 2025",
            "decree": "Decreto Presidencial 10/2025",
        },
    },
    {
        "title": "Política Nacional de Saúde Pública 2025-2030",
        "description": "Aprovação da nova política nacional de saúde pública",
        "decision_type": "policy",
        "status": "approved",
        "voting_record": {
            "votes_for": 22,
            "votes_against": 1,
            "abstentions": 2,
            "quorum": 0.92,
        },
        "meeting_id": COUNCIL_MEETING_1,
        "effective_date": datetime(2025, 2, 1, tzinfo=timezone.utc),
        "expiration_date": datetime(2030, 12, 31, tzinfo=timezone.utc),
        "related_documents": {
            "policy": "Política Nacional de Saúde 2025-2030",
            "decree": "Decreto Presidencial 11/2025",
        },
    },
    {
        "title": "Programa de Modernização de Infraestrutura Urbana",
        "description": "Aprovação do programa de investimento em infraestrutura urbana",
        "decision_type": "resolution",
        "status": "approved",
        "voting_record": {
            "votes_for": 18,
            "votes_against": 3,
            "abstentions": 4,
            "quorum": 0.72,
        },
        "meeting_id": COUNCIL_MEETING_1,
        "effective_date": datetime(2025, 3, 1, tzinfo=timezone.utc),
        "expiration_date": datetime(2028, 12, 31, tzinfo=timezone.utc),
        "related_documents": {
            "program": "Programa de Infraestrutura 2025-2028",
            "decree": "Decreto Presidencial 12/2025",
        },
    },
]


async def seed_institutions(session: AsyncSession) -> dict:
    """Seed institutions table with initial data."""
    logger.info("🌱 Iniciando seed de institutions...")

    created_count = 0
    skipped_count = 0

    for inst_data in DEFAULT_INSTITUTIONS:
        # Check if institution already exists (by ID)
        stmt = select(Institution).where(Institution.id == inst_data["id"])
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            logger.info(f"⏭️  Instituição '{inst_data['name']}' já existe, pulando...")
            skipped_count += 1
            continue

        # Create new institution
        institution = Institution(
            id=inst_data["id"],
            name=inst_data["name"],
            acronym=inst_data["acronym"],
            institution_type=inst_data["institution_type"],
            jurisdiction=inst_data["jurisdiction"],
            description=inst_data["description"],
            founding_date=inst_data["founding_date"],
            website=inst_data["website"],
            contact_info=inst_data["contact_info"],
            leadership=inst_data["leadership"],
            parent_institution_id=inst_data["parent_institution_id"],
        )
        session.add(institution)
        created_count += 1
        logger.info(f"✅ Instituição '{inst_data['name']}' criada")

    return {"created": created_count, "skipped": skipped_count}


async def seed_mandates(session: AsyncSession) -> dict:
    """Seed mandates table with initial data."""
    logger.info("🌱 Iniciando seed de mandates...")

    created_count = 0
    skipped_count = 0

    for mandate_data in DEFAULT_MANDATES:
        # Check if mandate already exists (by title and institution_id)
        stmt = select(Mandate).where(
            Mandate.title == mandate_data["title"],
            Mandate.institution_id == mandate_data["institution_id"],
        )
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            logger.info(f"⏭️  Mandato '{mandate_data['title']}' já existe, pulando...")
            skipped_count += 1
            continue

        # Create new mandate
        mandate = Mandate(
            title=mandate_data["title"],
            description=mandate_data["description"],
            mandate_type=mandate_data["mandate_type"],
            issuing_authority=mandate_data["issuing_authority"],
            start_date=mandate_data["start_date"],
            end_date=mandate_data["end_date"],
            status=mandate_data["status"],
            scope=mandate_data["scope"],
            related_documents=mandate_data["related_documents"],
            institution_id=mandate_data["institution_id"],
        )
        session.add(mandate)
        created_count += 1
        logger.info(f"✅ Mandato '{mandate_data['title']}' criado")

    return {"created": created_count, "skipped": skipped_count}


async def seed_council_meetings(session: AsyncSession) -> dict:
    """Seed council meetings table with initial data."""
    logger.info("🌱 Iniciando seed de council_meetings...")

    created_count = 0
    skipped_count = 0

    for meeting_data in DEFAULT_COUNCIL_MEETINGS:
        # Check if meeting already exists (by ID)
        stmt = select(CouncilMeeting).where(CouncilMeeting.id == meeting_data["id"])
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            logger.info(f"⏭️  Reunião '{meeting_data['title']}' já existe, pulando...")
            skipped_count += 1
            continue

        # Create new council meeting
        meeting = CouncilMeeting(
            id=meeting_data["id"],
            title=meeting_data["title"],
            description=meeting_data["description"],
            location=meeting_data["location"],
            start_time=meeting_data["start_time"],
            end_time=meeting_data["end_time"],
            status=meeting_data["status"],
            agenda=meeting_data["agenda"],
            minutes=meeting_data["minutes"],
            decisions=meeting_data["decisions"],
            participants=meeting_data["participants"],
            council_id=meeting_data["council_id"],
        )
        session.add(meeting)
        created_count += 1
        logger.info(f"✅ Reunião '{meeting_data['title']}' criada")

    return {"created": created_count, "skipped": skipped_count}


async def seed_decisions(session: AsyncSession) -> dict:
    """Seed decisions table with initial data."""
    logger.info("🌱 Iniciando seed de decisions...")

    created_count = 0
    skipped_count = 0

    for decision_data in DEFAULT_DECISIONS:
        # Check if decision already exists (by title and meeting_id)
        stmt = select(Decision).where(
            Decision.title == decision_data["title"],
            Decision.meeting_id == decision_data["meeting_id"],
        )
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            logger.info(f"⏭️  Decisão '{decision_data['title']}' já existe, pulando...")
            skipped_count += 1
            continue

        # Create new decision
        decision = Decision(
            title=decision_data["title"],
            description=decision_data["description"],
            decision_type=decision_data["decision_type"],
            status=decision_data["status"],
            voting_record=decision_data["voting_record"],
            meeting_id=decision_data["meeting_id"],
            effective_date=decision_data["effective_date"],
            expiration_date=decision_data["expiration_date"],
            related_documents=decision_data["related_documents"],
        )
        session.add(decision)
        created_count += 1
        logger.info(f"✅ Decisão '{decision_data['title']}' criada")

    return {"created": created_count, "skipped": skipped_count}


async def seed_all():
    """Seed all governance tables with initial data."""
    logger.info("🚀 Iniciando seed completo do módulo Governance...")

    async with AsyncSessionLocal() as session:
        try:
            results = {}

            # Seed in order (respecting dependencies)
            results["institutions"] = await seed_institutions(session)
            await session.commit()

            results["mandates"] = await seed_mandates(session)
            await session.commit()

            results["council_meetings"] = await seed_council_meetings(session)
            await session.commit()

            results["decisions"] = await seed_decisions(session)
            await session.commit()

            # Summary
            total_created = sum(r["created"] for r in results.values())
            total_skipped = sum(r["skipped"] for r in results.values())

            logger.info("🎉 Seed completo concluído!")
            logger.info(f"   📊 Total criado: {total_created}")
            logger.info(f"   ⏭️  Total já existia: {total_skipped}")
            logger.info(
                f"   📋 Instituições: {results['institutions']['created']} criadas, {results['institutions']['skipped']} já existiam"
            )
            logger.info(
                f"   📋 Mandatos: {results['mandates']['created']} criados, {results['mandates']['skipped']} já existiam"
            )
            logger.info(
                f"   📋 Reuniões: {results['council_meetings']['created']} criadas, {results['council_meetings']['skipped']} já existiam"
            )
            logger.info(
                f"   📋 Decisões: {results['decisions']['created']} criadas, {results['decisions']['skipped']} já existiam"
            )

            return results

        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Erro ao fazer seed: {e}")
            raise


async def main():
    """Main entry point for seed script."""
    try:
        results = await seed_all()
        print(f"\n✅ Seed concluído com sucesso!")
        print(f"   📊 Total criado: {sum(r['created'] for r in results.values())}")
        print(f"   ⏭️  Total já existia: {sum(r['skipped'] for r in results.values())}")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro ao executar seed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
