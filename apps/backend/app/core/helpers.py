"""
Shared helpers for safe attribute access across modules.

Provides utilities for null-safe field access, isoformat conversion,
and enum handling to prevent AttributeError crashes in APIs.
"""
from typing import Any, Optional, TypeVar

T = TypeVar('T')


def safe_get(obj: Any, attr: str, default: Optional[T] = None) -> Optional[T]:
    """
    Safely retrieves an attribute from an object.
    
    Returns default value if attribute doesn't exist or object is None.
    
    Args:
        obj: Object to retrieve attribute from
        attr: Attribute name
        default: Default value if attribute missing
    
    Returns:
        Attribute value or default
    
    Example:
        >>> safe_get(citizen, "email", "no-email@example.com")
        "john@example.com"
    """
    if obj is None:
        return default
    return getattr(obj, attr, default)


def safe_isoformat(value: Any) -> Optional[str]:
    """
    Safely convert datetime/date object to ISO format string.
    
    Returns None if value is None or conversion fails.
    
    Args:
        value: datetime, date, or other object with isoformat() method
    
    Returns:
        ISO format string or None
    
    Example:
        >>> safe_isoformat(datetime.now())
        "2026-02-16T10:30:45.123456"
    """
    if value is None:
        return None
    try:
        return value.isoformat()
    except (AttributeError, TypeError):
        return None


def safe_str(value: Any) -> Optional[str]:
    """
    Safely convert any value to string.
    
    Returns None if value is None.
    
    Args:
        value: Any value
    
    Returns:
        String representation or None
    """
    if value is None:
        return None
    try:
        return str(value)
    except Exception:
        return None


def safe_enum_value(value: Any) -> Optional[str]:
    """
    Safely extract enum value from enum object.
    
    Returns the .value property if it exists, otherwise the original value.
    Returns None if value is None.
    
    Args:
        value: Enum or regular object
    
    Returns:
        Enum value or original value
    
    Example:
        >>> from enum import Enum
        >>> class Status(str, Enum):
        ...     ACTIVE = "active"
        >>> safe_enum_value(Status.ACTIVE)
        "active"
    """
    if value is None:
        return None
    return getattr(value, "value", value)


class SafeMapper:
    """Helper class to safely map object attributes to dictionaries."""
    
    @staticmethod
    def to_dict(obj: Any, field_spec: dict[str, tuple[str, type]]) -> dict:
        """
        Safely map object attributes to dictionary.
        
        Args:
            obj: Object to map
            field_spec: Dict mapping output key to (input_attr, converter_func)
                       Converter can be: safe_get, safe_isoformat, safe_str, safe_enum_value, or callable
        
        Returns:
            Mapped dictionary with safe getters and type conversions
        
        Example:
            >>> mapping = {
            ...     "id": ("citizen_id", safe_str),
            ...     "name": ("full_name", safe_get),
            ...     "birth": ("birth_date", safe_isoformat),
            ...     "status": ("vital_status", safe_enum_value),
            ... }
            >>> result = SafeMapper.to_dict(citizen, mapping)
        """
        result = {}
        for output_key, (input_attr, converter) in field_spec.items():
            value = safe_get(obj, input_attr)
            if callable(converter) and converter not in [safe_get, safe_isoformat, safe_str, safe_enum_value]:
                # Custom callable converter
                result[output_key] = converter(value)
            elif converter == safe_isoformat:
                result[output_key] = safe_isoformat(value)
            elif converter == safe_str:
                result[output_key] = safe_str(value)
            elif converter == safe_enum_value:
                result[output_key] = safe_enum_value(value)
            else:
                # Default: just return the value
                result[output_key] = value
        return result
