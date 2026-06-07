from __future__ import annotations

import os
import uuid


def current_region_code() -> str:
    return (os.environ.get("OP_REGION_CODE") or "A").strip().upper()


def generate_global_id(region_code: str | None = None) -> str:
    code = (region_code or current_region_code()).strip().upper()
    return f"{code}-{uuid.uuid4()}"
