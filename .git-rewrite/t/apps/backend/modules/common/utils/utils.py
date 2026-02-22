"""
Common utility functions for the SILA system.

This module provides general-purpose utility functions that can be used
across all modules to reduce code duplication and ensure consistency.
"""

import hashlib
import re
import secrets
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from passlib.context import CryptContext

# Security utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_hex(length)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def generate_api_key() -> str:
    """Generate a secure API key."""
    return f"sk-{secrets.token_urlsafe(32)}"


# Validation utilities
def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    pattern = r"^\+?[1-9]\d{1,14}$"
    return re.match(pattern, phone) is not None


def validate_nif(nif: str) -> bool:
    clean_nif = re.sub(r"\D", "", nif)
    return len(clean_nif) == 10


def validate_bi_number(bi_number: str) -> bool:
    clean_bi = re.sub(r"[^A-Za-z0-9]", "", bi_number)
    return 8 <= len(clean_bi) <= 14


# String utilities
def normalize_string(text: str, remove_accents: bool = False) -> str:
    import unicodedata

    normalized = " ".join(text.split())

    if remove_accents:
        normalized = unicodedata.normalize("NFKD", normalized)
        normalized = "".join(c for c in normalized if not unicodedata.combining(c))

    return normalized.strip()


def generate_slug(text: str) -> str:
    slug = normalize_string(text, remove_accents=True).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")

    if len(slug) > 100:
        slug = slug[:100].rstrip("-")

    return slug


def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 4) -> str:
    if len(data) <= visible_chars:
        return mask_char * len(data)

    masked_length = len(data) - visible_chars
    return mask_char * masked_length + data[-visible_chars:]


# Date/time utilities
def format_datetime_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def parse_datetime_iso(dt_string: str) -> datetime:
    return datetime.fromisoformat(dt_string.replace("Z", "+00:00"))


def get_age_from_birthdate(birthdate: datetime) -> int:
    today = datetime.now(timezone.utc)
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age


# Data transformation utilities
def clean_document_number(document_number: str) -> str:
    return re.sub(r"[^\w]", "", document_number).upper()


def extract_numbers(text: str) -> str:
    return re.sub(r"\D", "", text)


def format_currency(amount: Union[int, float], currency: str = "AOA") -> str:
    return f"{amount:,.2f} {currency}"


# Dictionary utilities
def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def flatten_dict(
    d: Dict[str, Any], parent_key: str = "", sep: str = "."
) -> Dict[str, Any]:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# List utilities
def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def remove_duplicates(lst: List[Any], key: Optional[str] = None) -> List[Any]:
    if key is None:
        return list(dict.fromkeys(lst))
    else:
        seen = set()
        result = []
        for item in lst:
            if isinstance(item, dict) and key in item:
                if item[key] not in seen:
                    seen.add(item[key])
                    result.append(item)
            else:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
        return result


# Hash utilities
def generate_hash(data: str, algorithm: str = "sha256") -> str:
    hash_func = getattr(hashlib, algorithm)()
    hash_func.update(data.encode("utf-8"))
    return hash_func.hexdigest()


def verify_hash(data: str, hash_value: str, algorithm: str = "sha256") -> bool:
    return generate_hash(data, algorithm) == hash_value


# UUID utilities
def is_valid_uuid(uuid_string: str) -> bool:
    try:
        UUID(uuid_string)
        return True
    except ValueError:
        return False


def generate_short_uuid() -> str:
    return str(uuid4())[:8]


# Error handling utilities
def safe_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
    return dictionary.get(key, default)


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


__all__ = [
    # Security
    "generate_secure_token",
    "hash_password",
    "verify_password",
    "generate_api_key",
    # Validation
    "validate_email",
    "validate_phone",
    "validate_nif",
    "validate_bi_number",
    # String
    "normalize_string",
    "generate_slug",
    "mask_sensitive_data",
    # Date/Time
    "format_datetime_iso",
    "parse_datetime_iso",
    "get_age_from_birthdate",
    # Data transformation
    "clean_document_number",
    "extract_numbers",
    "format_currency",
    # Dictionary
    "deep_merge_dicts",
    "flatten_dict",
    # List
    "chunk_list",
    "remove_duplicates",
    # Hash
    "generate_hash",
    "verify_hash",
    # UUID
    "is_valid_uuid",
    "generate_short_uuid",
    # Error handling
    "safe_get",
    "safe_int",
    "safe_float",
]
