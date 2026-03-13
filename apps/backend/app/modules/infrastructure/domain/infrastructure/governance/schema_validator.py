from __future__ import annotations
from typing import Any

def validate_payload(payload: dict[str, Any], schema: dict) -> bool:
    try:
        from fastavro.validation import validate as avro_validate
    except Exception:
        return _fallback_validate(payload, schema)
    try:
        return bool(avro_validate(payload, schema))
    except Exception:
        return False

def _fallback_validate(payload: dict[str, Any], schema: dict) -> bool:
    fields = list(schema.get('fields') or [])
    for field in fields:
        name = str(field.get('name') or '')
        field_type = field.get('type')
        if not name:
            return False
        if name not in payload:
            return False
        if not _check_type(payload[name], field_type):
            return False
    return True

def _check_type(value: Any, field_type: Any) -> bool:
    if field_type == 'string':
        return isinstance(value, str)
    if field_type == 'int':
        return isinstance(value, int) and (not isinstance(value, bool))
    if field_type == 'long':
        return isinstance(value, int) and (not isinstance(value, bool))
    if field_type == 'float':
        return isinstance(value, (int, float)) and (not isinstance(value, bool))
    if field_type == 'double':
        return isinstance(value, (int, float)) and (not isinstance(value, bool))
    if field_type == 'boolean':
        return isinstance(value, bool)
    return True