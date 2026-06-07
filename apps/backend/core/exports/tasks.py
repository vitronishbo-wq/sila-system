import asyncio
import json
from typing import Any

from apps.backend.app.core.db import AsyncSessionLocal
from apps.backend.app.platform.runtime.compat_router import (
    _build_citizens_export_bytes,
    _build_documents_export_bytes,
)
from core.celery import app as celery_app
from sqlalchemy import text


async def _fetch_job(session, job_id: str) -> dict[str, Any] | None:
    result = await session.execute(
        text("""
            SELECT id, module, owner_id, status, request_payload
            FROM export_jobs
            WHERE id = :job_id
            LIMIT 1
        """),
        {"job_id": job_id},
    )
    row = result.mappings().first()
    return dict(row) if row else None


async def _update_job(session, job_id: str, status_value: str, **fields: Any) -> None:
    await session.execute(
        text("""
            UPDATE export_jobs
            SET status = :status,
                result_data = COALESCE(:result_data, result_data),
                result_content_type = COALESCE(:result_content_type, result_content_type),
                result_filename = COALESCE(:result_filename, result_filename),
                error = COALESCE(:error, error),
                updated_at = now()
            WHERE id = :job_id
        """),
        {
            "status": status_value,
            "result_data": fields.get("result_data"),
            "result_content_type": fields.get("result_content_type"),
            "result_filename": fields.get("result_filename"),
            "error": fields.get("error"),
            "job_id": job_id,
        },
    )


async def _log_job(session, job_id: str, level: str, message: str) -> None:
    await session.execute(
        text("""
            INSERT INTO export_job_logs (id, job_id, level, message, created_at)
            VALUES (gen_random_uuid(), :job_id, :level, :message, now())
        """),
        {"job_id": job_id, "level": level, "message": message},
    )


async def _run_export(job_id: str) -> None:
    async with AsyncSessionLocal() as session:
        job = await _fetch_job(session, job_id)
        if not job:
            return
        await _log_job(session, job_id, "info", "Job started")
        await _update_job(session, job_id, "running")
        await session.commit()
        payload = job.get("request_payload") or {}
        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                payload = {}
        params = payload.get("params", {})
        columns = payload.get("columns")
        export_format = payload.get("format", "csv")
        try:
            if job.get("module") == "citizens":
                data, content_type, filename = await _build_citizens_export_bytes(
                    session,
                    params,
                    columns,
                    export_format,
                )
            else:
                data, content_type, filename = await _build_documents_export_bytes(
                    session,
                    params,
                    columns,
                    export_format,
                )
            await _update_job(
                session,
                job_id,
                "done",
                result_data=data,
                result_content_type=content_type,
                result_filename=filename,
            )
            await _log_job(session, job_id, "info", f"Job completed ({filename})")
            await session.commit()
        except Exception as exc:
            await _update_job(session, job_id, "failed", error=str(exc))
            await _log_job(session, job_id, "error", f"Job failed: {exc}")
            await session.commit()


@celery_app.task(name="core.exports.run_export_job")
def run_export_job(job_id: str) -> None:
    asyncio.run(_run_export(job_id))
