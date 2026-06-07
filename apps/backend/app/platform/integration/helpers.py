MOCK_PLACEHOLDER_PREFIXES = ("MOCK_", "PLACEHOLDER_", "DEV_")


def is_placeholder_key(key: str | None) -> bool:
    if not key:
        return True
    upper = key.upper().strip()
    for prefix in MOCK_PLACEHOLDER_PREFIXES:
        if upper.startswith(prefix):
            return True
    return False


def mock_reason(key: str | None, key_name: str = "api_key") -> str:
    if not key:
        return f"{key_name} não configurado"
    if is_placeholder_key(key):
        return f"{key_name} com placeholder ({key[:20]}...)"
    return f"{key_name} configurado (potencialmente válido)"
