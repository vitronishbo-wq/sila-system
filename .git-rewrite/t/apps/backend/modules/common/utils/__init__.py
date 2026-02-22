"""Common utilities module."""

from .utils import (
    # Security
    generate_secure_token,
    hash_password,
    verify_password,
    generate_api_key,
    # Validation
    validate_email,
    validate_phone,
    validate_nif,
    validate_bi_number,
    # String
    normalize_string,
    generate_slug,
    mask_sensitive_data,
    # Date/Time
    format_datetime_iso,
    parse_datetime_iso,
    get_age_from_birthdate,
    # Data transformation
    clean_document_number,
    extract_numbers,
    format_currency,
    # Dictionary
    deep_merge_dicts,
    flatten_dict,
    # List
    chunk_list,
    remove_duplicates,
    # Hash
    generate_hash,
    verify_hash,
    # UUID
    is_valid_uuid,
    generate_short_uuid,
    # Error handling
    safe_get,
    safe_int,
    safe_float,
)

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
