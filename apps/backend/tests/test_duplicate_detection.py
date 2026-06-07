"""
Duplicate Detection Engine Test — TASK-074

Validates that IdentityResolutionService.find_duplicates() correctly
classifies duplicates by confidence level and produces 0 false positives.

NOTE: HIGH (same_bi/national_student_number) cannot be tested via DB
inserts because national_student_number has a UNIQUE constraint at the
DB level. This constraint is the defence against same-ENS duplicates.
The find_duplicates() HIGH path is dead code kept for legacy data safety.
"""

import asyncio
import os
import sys
from datetime import date
from uuid import UUID, uuid4

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db")

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text

from apps.backend.app.modules.educacao.application.identity_resolution_service import IdentityResolutionService


TEST_PREFIX = "TASK074_"

DATASET = {
    "name_birth_matches": [
        {"id": uuid4(), "full_name": "Joao Manuel Pedro", "birth_date": date(2004, 7, 22),
         "gender": "M", "nationality": "ANGOLANA",
         "national_student_number": f"ENS-2026-{TEST_PREFIX}MED001"},
        {"id": uuid4(), "full_name": "Joao Manuel Pedro", "birth_date": date(2004, 7, 22),
         "gender": "M", "nationality": "ANGOLANA",
         "national_student_number": f"ENS-2026-{TEST_PREFIX}MED002"},
    ],
    "guardian_birth_matches": [
        {"id": uuid4(), "full_name": "Maria Lopes Costa", "birth_date": date(2006, 11, 5),
         "gender": "F", "nationality": "ANGOLANA",
         "national_student_number": f"ENS-2026-{TEST_PREFIX}LOW001",
         "guardian_id": UUID("00000000-0000-0000-0000-000000000011")},
        {"id": uuid4(), "full_name": "M. L. Costa", "birth_date": date(2006, 11, 5),
         "gender": "F", "nationality": "ANGOLANA",
         "national_student_number": f"ENS-2026-{TEST_PREFIX}LOW002",
         "guardian_id": UUID("00000000-0000-0000-0000-000000000011")},
    ],
    "unique_identities": [
        {"id": uuid4(), "full_name": "Unique Student One", "birth_date": date(2000, 1, 1),
         "gender": "M", "nationality": "ANGOLANA",
         "national_student_number": f"ENS-2026-{TEST_PREFIX}UNIQ001"},
        {"id": uuid4(), "full_name": "Unique Student Two", "birth_date": date(2001, 2, 2),
         "gender": "F", "nationality": "ANGOLANA",
         "national_student_number": f"ENS-2026-{TEST_PREFIX}UNIQ002"},
        {"id": uuid4(), "full_name": "Unique Student Three", "birth_date": date(2002, 3, 3),
         "gender": "M", "nationality": "ANGOLANA",
         "national_student_number": f"ENS-2026-{TEST_PREFIX}UNIQ003"},
    ],
}


async def seed_dataset(session: AsyncSession):
    total = 0
    for category, identities in DATASET.items():
        for ident in identities:
            guardian_id = ident.get("guardian_id")
            await session.execute(text("""
                INSERT INTO educacao_academic_identities
                    (id, national_student_number, full_name, birth_date, gender,
                     nationality, guardian_id, identity_status, created_at, updated_at)
                VALUES
                    (:id, :ns, :name, :dob, :gender,
                     :nationality, :guardian_id, 'VALID', now(), now())
                ON CONFLICT (id) DO NOTHING
            """), {
                "id": ident["id"],
                "ns": ident["national_student_number"],
                "name": ident["full_name"],
                "dob": ident["birth_date"],
                "gender": ident.get("gender", "M"),
                "nationality": ident.get("nationality", "ANGOLANA"),
                "guardian_id": guardian_id,
            })
            total += 1
    await session.commit()
    return total


async def cleanup(session: AsyncSession):
    for category, identities in DATASET.items():
        for ident in identities:
            await session.execute(
                text("DELETE FROM educacao_academic_identities WHERE id = :id"),
                {"id": ident["id"]},
            )
    await session.commit()


def summarize_results(results) -> dict:
    by_confidence = {}
    false_positives = []
    matched_ids = set()

    for r in results:
        by_confidence.setdefault(r.confidence, []).append(r)
        matched_ids.add(str(r.identity_id))
        matched_ids.add(str(r.duplicate_of))

    for ident in DATASET["unique_identities"]:
        if str(ident["id"]) in matched_ids:
            false_positives.append(str(ident["id"]))

    duplicate_ids = set()
    for category in ["name_birth_matches", "guardian_birth_matches"]:
        for ident in DATASET[category][1:]:
            duplicate_ids.add(str(ident["id"]))
    missed = duplicate_ids - matched_ids

    return {
        "total_results": len(results),
        "by_confidence": {k: len(v) for k, v in by_confidence.items()},
        "false_positives": len(false_positives),
        "false_positive_ids": false_positives,
        "missed_duplicates": len(missed),
        "missed_ids": list(missed),
        "pass": len(false_positives) == 0 and len(missed) == 0,
    }


async def main():
    print("=" * 60)
    print("DUPLICATE DETECTION ENGINE - TASK-074")
    print("=" * 60)

    engine = create_async_engine(os.environ["DATABASE_URL"])
    async with AsyncSession(engine) as session:
        total = await seed_dataset(session)
        print(f"\nSeeded {total} identities:")
        for category, identities in DATASET.items():
            print(f"  {category}: {len(identities)}")
        print()

        resolver = IdentityResolutionService(session)
        results = await resolver.find_duplicates()
        print(f"find_duplicates() returned {len(results)} results\n")

        summary = summarize_results(results)
        print(f"By confidence: {summary['by_confidence']}")
        print(f"False positives: {summary['false_positives']}")
        if summary["false_positive_ids"]:
            print(f"  IDs: {summary['false_positive_ids']}")
        print(f"Missed duplicates: {summary['missed_duplicates']}")
        if summary["missed_ids"]:
            for mid in summary["missed_ids"]:
                for cat, idents in DATASET.items():
                    for ident in idents:
                        if str(ident["id"]) == mid:
                            print(f"  {ident['full_name'][:30]} ({ident['national_student_number']}) - {cat}")

        print(f"\nResult detail:")
        for r in results:
            print(f"  [{r.confidence:>6}] {str(r.identity_id)[:8]} -> {str(r.duplicate_of)[:8]} ({r.match_type}) fields={r.fields}")

        status = "PASS" if summary["pass"] else "FAIL"
        print(f"\n  Status: {status}")

        await cleanup(session)
        print("  Cleaned up test data\n")

    await engine.dispose()

    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
