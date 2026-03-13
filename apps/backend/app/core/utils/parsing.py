"""Null-safe parsing helpers (split from legacy helpers.py)."""
from typing import Any, Optional, TypeVar
T = TypeVar('T')

def safe_get(obj: Any, attr: str, default: Optional[T]=None) -> Optional[T]:
    """Retorna atributo se existir; caso contrário retorna default."""
    if obj is None:
        return default
    return getattr(obj, attr, default)

def safe_str(value: Any) -> str | None:
    """Converte valor para str de forma segura."""
    if value is None:
        return None
    try:
        return str(value)
    except Exception:
        return None

def safe_enum_value(value: Any) -> Any:
    """Extrai `.value` de enums, mantendo fallback para objetos comuns."""
    if value is None:
        return None
    return getattr(value, 'value', value)

class SafeMapper:
    """Mapeador seguro de atributos para dicionário."""

    @staticmethod
    def to_dict(obj: Any, field_spec: dict[str, tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for output_key, (input_attr, converter) in field_spec.items():
            value = safe_get(obj, input_attr)
            if callable(converter):
                result[output_key] = converter(value)
            else:
                result[output_key] = value
        return result