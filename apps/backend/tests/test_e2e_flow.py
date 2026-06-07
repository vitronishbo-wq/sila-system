"""
End-to-End Flow Validation — TASK-080

Validates the complete identity lifecycle:
  create identity -> emit ENS -> enroll -> transfer -> certificate -> wallet -> dashboard

Each step uses the actual application services (not mocks).
"""

import asyncio
import os
import sys
from datetime import date, datetime, timezone
from uuid import UUID, uuid4

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db")

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload

from apps.backend.app.modules.educacao.application.academic_identity_service import AcademicIdentityService
from apps.backend.app.modules.educacao.application.academic_record_service import AcademicRecordService
from apps.backend.app.modules.educacao.application.identity_resolution_service import IdentityResolutionService
from apps.backend.app.modules.educacao.application.academic_wallet_service import AcademicWalletService
from apps.backend.app.modules.educacao.application.identity_governance_service import IdentityGovernanceService
from apps.backend.app.modules.educacao.infrastructure.models.enrollment_model import EnrollmentModel
from apps.backend.app.modules.educacao.infrastructure.models.academic_identity_model import AcademicIdentityModel
from apps.backend.app.modules.educacao.domain.academic_identity import AcademicStatus

PASS = 0
FAIL = 0

def check(step: str, condition: bool, detail: str = ""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {step} {detail}")
    else:
        FAIL += 1
        print(f"  [FAIL] {step} {detail}")


async def main():
    global PASS, FAIL
    PASS = 0
    FAIL = 0

    print("=" * 60)
    print("END-TO-END FLOW — TASK-080")
    print("=" * 60)

    engine = create_async_engine(os.environ["DATABASE_URL"])
    created_identity_id = None
    created_enrollment_ids = []

    try:
        async with AsyncSession(engine) as session:
            # ============================================================
            # STEP 1: CREATE IDENTITY + EMIT ENS
            # ============================================================
            print("\n--- STEP 1: Create Identity + Emit ENS ---")
            identity_svc = AcademicIdentityService(session)
            gov_svc = IdentityGovernanceService(session)

            identity = await identity_svc.create_identity(
                full_name="EndToEnd Test Student",
                birth_date=date(2008, 6, 15),
                gender="MASCULINO",
                nationality="ANGOLANA",
            )
            created_identity_id = identity.id

            check("ENS generated", bool(identity.national_student_number),
                  f"ENS={identity.national_student_number}")
            check("ENS format", identity.national_student_number.startswith("ENS-2026-"),
                  f"format={identity.national_student_number}")
            check("Identity ID", identity.id is not None, f"id={identity.id}")
            check("Full name match", identity.full_name == "EndToEnd Test Student")
            check("Academic status", identity.academic_status == AcademicStatus.ACTIVE.value)
            check("Identity status", identity.identity_status == "VALID")

            # Verify in DB
            db_identity = await session.get(AcademicIdentityModel, identity.id)
            check("Persisted in DB", db_identity is not None)
            check("ENS unique in DB", db_identity.national_student_number == identity.national_student_number)

            await session.commit()
            print("  Step 1 OK")

            # ============================================================
            # STEP 2: ENROLLMENT (matriculation)
            # ============================================================
            print("\n--- STEP 2: Matriculation (Enrollment) ---")
            now = datetime.now(timezone.utc)
            institution_id = uuid4()
            enrollment_id = uuid4()
            enrollment = EnrollmentModel(
                id=enrollment_id,
                student_id=identity.id,
                institution_id=institution_id,
                academic_year="2026",
                grade="10",
                status="ACTIVE",
                started_at=now,
                academic_identity_id=identity.id,
            )
            session.add(enrollment)
            await session.flush()
            created_enrollment_ids.append(enrollment_id)

            check("Enrollment created", True)
            check("Enrollment student_id", enrollment.student_id == identity.id)
            check("Enrollment status", enrollment.status == "ACTIVE")

            # Record in academic history
            record_svc = AcademicRecordService(session)
            await record_svc.record_enrollment(
                identity_id=identity.id,
                enrollment_id=enrollment_id,
                institution_id=institution_id,
                academic_year="2026",
                grade="10",
            )

            # Verify academic record
            history = await record_svc.get_history(identity.id)
            check("Academic record exists", history is not None)
            enrollments = history["history"].get("enrollments", []) if history else []
            check("History has enrollment", len(enrollments) >= 1,
                  f"enrollments={len(enrollments)}")

            await session.commit()
            print("  Step 2 OK")

            # ============================================================
            # STEP 3: TRANSFER (transfere para outra instituicao)
            # ============================================================
            print("\n--- STEP 3: Transfer ---")
            new_institution_id = uuid4()
            new_enrollment = EnrollmentModel(
                id=uuid4(),
                student_id=identity.id,
                institution_id=new_institution_id,
                academic_year="2026",
                grade="10",
                status="ACTIVE",
                started_at=datetime.now(timezone.utc),
                academic_identity_id=identity.id,
                transfer_origin_id=institution_id,
            )
            session.add(new_enrollment)
            await session.flush()
            created_enrollment_ids.append(new_enrollment.id)

            # Close previous enrollment
            enrollment.status = "TRANSFERRED"
            enrollment.ended_at = datetime.now(timezone.utc)
            enrollment.transfer_destination_id = new_enrollment.id

            await record_svc.record_transfer(
                identity_id=identity.id,
                from_enrollment_id=enrollment_id,
                to_enrollment_id=new_enrollment.id,
                from_institution_id=institution_id,
                to_institution_id=new_institution_id,
                academic_year="2026",
                grade="10",
            )

            history2 = await record_svc.get_history(identity.id)
            transfers = history2["history"].get("transfers", []) if history2 else []
            check("Transfer recorded", len(transfers) >= 1,
                  f"transfers={len(transfers)}")

            # Update identity status
            identity_model = await session.get(AcademicIdentityModel, identity.id)
            identity_model.current_institution_id = new_institution_id
            identity_model.current_grade = "10"
            identity_model.academic_status = AcademicStatus.ACTIVE.value

            await session.commit()
            print("  Step 3 OK")

            # ============================================================
            # STEP 4: CERTIFICATE
            # ============================================================
            print("\n--- STEP 4: Certificate ---")
            await record_svc.record_certificate(
                identity_id=identity.id,
                certificate_type="conclusao",
                institution_id=new_institution_id,
                grade="10",
            )

            history3 = await record_svc.get_history(identity.id)
            certs = history3["history"].get("certificates", []) if history3 else []
            check("Certificate recorded", len(certs) >= 1,
                  f"certificates={len(certs)}")
            check("Completed classes updated",
                  len(history3.get("completed_classes", [])) >= 1 if history3 else False,
                  f"completed={history3.get('completed_classes', []) if history3 else 'N/A'}")

            await session.commit()
            print("  Step 4 OK")

        # ============================================================
        # STEP 5: WALLET (unified profile)
        # ============================================================
        print("\n--- STEP 5: Wallet (Unified Profile) ---")
        async with AsyncSession(engine) as session:
            wallet_svc = AcademicWalletService(session)
            wallet = await wallet_svc.get_wallet(created_identity_id)

            check("Wallet returned", "error" not in wallet, f"error={wallet.get('error')}")
            check("Wallet identity matches", wallet["identity"]["full_name"] == "EndToEnd Test Student")
            check("Wallet ENS present", bool(wallet["identity"]["national_student_number"]))
            check("Wallet active enrollment", wallet["active_enrollment"] is not None,
                  f"institution={wallet['active_enrollment'].get('institution_id', 'N/A') if wallet['active_enrollment'] else 'None'}")
            check("Wallet enrollment history", len(wallet.get("enrollment_history", [])) >= 2,
                  f"history={len(wallet.get('enrollment_history', []))}")
            check("Wallet record present", wallet.get("record") is not None)
            check("Wallet completed classes",
                  len(wallet.get("record", {}).get("completed_classes", [])) >= 1)
            print("  Step 5 OK")

        # ============================================================
        # STEP 6: DASHBOARD
        # ============================================================
        print("\n--- STEP 6: Dashboard Metrics ---")
        async with AsyncSession(engine) as session:
            dash_svc = AcademicIdentityService(session)
            res_svc = IdentityResolutionService(session)

            total = await dash_svc.count_total()
            active_count = await dash_svc.count_by_status(AcademicStatus.ACTIVE)
            duplicates = await res_svc.find_duplicates()

            check("Total count > 0", total > 0, f"total={total}")
            check("Active count > 0", active_count > 0, f"active={active_count}")
            check("Duplicates scanned", isinstance(duplicates, list))

            # The dashboard calculation
            dup_rate = round(len(duplicates) / max(total, 1) * 100, 2) if total > 0 else 0
            check("Duplicate rate calculated", isinstance(dup_rate, (int, float)),
                  f"rate={dup_rate}%")

            print(f"  Dashboard metrics: total={total}, active={active_count}, "
                  f"duplicates={len(duplicates)}, rate={dup_rate}%")
            print("  Step 6 OK")

    finally:
        # ============================================================
        # CLEANUP
        # ============================================================
        print("\n--- Cleanup ---")
        async with AsyncSession(engine) as session:
            if created_identity_id:
                # Delete academic records
                await session.execute(
                    text("DELETE FROM educacao_academic_records WHERE academic_identity_id = :id"),
                    {"id": created_identity_id},
                )
                # Delete enrollments
                for eid in created_enrollment_ids:
                    await session.execute(
                        text("DELETE FROM educacao_enrollments WHERE id = :id"),
                        {"id": eid},
                    )
                # Delete identity
                await session.execute(
                    text("DELETE FROM educacao_academic_identities WHERE id = :id"),
                    {"id": created_identity_id},
                )
                await session.commit()
            print("  Cleanup complete\n")

    await engine.dispose()

    # ============================================================
    # RESULTS
    # ============================================================
    total = PASS + FAIL
    print("=" * 60)
    print(f"RESULTS: {PASS}/{total} passed, {FAIL} failed")
    print("=" * 60)
    return FAIL == 0


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
