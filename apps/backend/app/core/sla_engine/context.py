from __future__ import annotations

from typing import Any, Dict

from .models import SLAContext


def build_context(payload: Dict[str, Any], current_user: Dict[str, Any] | None = None) -> SLAContext:
    data = dict(payload or {})
    user = current_user or {}

    if "province" not in data:
        province = user.get("province") or user.get("territory") or user.get("territory_id")
        if province:
            data["province"] = str(province).lower()
    if "citizen_type" not in data:
        citizen_type = user.get("citizen_type") or user.get("profile_type")
        if citizen_type:
            data["citizen_type"] = str(citizen_type).lower()
    if "channel" not in data:
        channel = user.get("channel") or "online"
        data["channel"] = str(channel).lower()

    return SLAContext(**data)
