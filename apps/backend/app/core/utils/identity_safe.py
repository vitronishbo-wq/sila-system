"""
Utilitários de Acesso Seguro (Safe Helpers)

Fornece funções para acesso seguro a atributos de objetos,
evitando AttributeError e facilitando acesso a valores opcionais.
"""

from collections.abc import Callable
from datetime import date, datetime
from typing import Any, TypeVar

T = TypeVar("T")


def safe_get(obj: Any, attr_name: str, default: Any = None) -> Any:
    """
    Acesso seguro a atributo de objeto, retornando valor padrão se não existir.

    Args:
        obj: Objeto do qual acessar o atributo.
        attr_name: Nome do atributo.
        default: Valor padrão se o atributo não existir.

    Returns:
        Valor do atributo ou default.

    Examples:
        >>> class User:
        ...     name = "João"
        >>> user = User()
        >>> safe_get(user, "name")
        "João"
        >>> safe_get(user, "age", 0)
        0
    """
    try:
        if isinstance(obj, dict):
            return obj.get(attr_name, default)
        return getattr(obj, attr_name, default)
    except (AttributeError, TypeError):
        return default


def safe_getitem(obj: dict, key: str, default: Any = None) -> Any:
    """
    Acesso seguro a item de dicionário.

    Args:
        obj: Dicionário do qual acessar a chave.
        key: Chave a acessar.
        default: Valor padrão se a chave não existir.

    Returns:
        Valor da chave ou default.

    Examples:
        >>> data = {"name": "Maria"}
        >>> safe_getitem(data, "name")
        "Maria"
        >>> safe_getitem(data, "age", 18)
        18
    """
    if not isinstance(obj, dict):
        return default
    return obj.get(key, default)


def safe_isoformat(dt: datetime | None) -> str | None:
    """
    Converte datetime/date para ISO format de forma segura.

    Args:
        dt: Objeto datetime ou date.

    Returns:
        String em formato ISO ou None.

    Examples:
        >>> from datetime import date
        >>> d = date(2026, 2, 16)
        >>> safe_isoformat(d)
        "2026-02-16"
        >>> safe_isoformat(None)
        None
    """
    if dt is None:
        return None
    try:
        if isinstance(dt, (datetime, date)):
            return dt.isoformat()
        return None
    except (AttributeError, TypeError):
        return None


def safe_int(value: Any, default: int = 0) -> int:
    """
    Converte valor para inteiro de forma segura.

    Args:
        value: Valor a converter.
        default: Valor padrão se conversão falhar.

    Returns:
        Inteiro ou default.

    Examples:
        >>> safe_int("42")
        42
        >>> safe_int("invalid", -1)
        -1
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Converte valor para float de forma segura.

    Args:
        value: Valor a converter.
        default: Valor padrão se conversão falhar.

    Returns:
        Float ou default.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_str(value: Any, default: str = "") -> str:
    """
    Converte valor para string de forma segura.

    Args:
        value: Valor a converter.
        default: Valor padrão se conversão falhar.

    Returns:
        String ou default.
    """
    if value is None:
        return default
    try:
        return str(value)
    except (ValueError, TypeError):
        return default


def safe_bool(value: Any, default: bool = False) -> bool:
    """
    Converte valor para bool de forma segura.

    Args:
        value: Valor a converter.
        default: Valor padrão se conversão falhar.

    Returns:
        Bool ou default.
    """
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "sim", "on")
    if isinstance(value, (int, float)):
        return bool(value)
    return default


def safe_apply(obj: Any, attr_name: str, transformer: Callable[[Any], T], default: T = None) -> T:
    """
    Aplica uma função de transformação a um atributo de forma segura.

    Args:
        obj: Objeto do qual acessar o atributo.
        attr_name: Nome do atributo.
        transformer: Função para transformar o valor.
        default: Valor padrão se falhar.

    Returns:
        Valor transformado ou default.

    Examples:
        >>> class Product:
        ...     price = "19.99"
        >>> product = Product()
        >>> safe_apply(product, "price", float)
        19.99
        >>> safe_apply(product, "discount", float, 0.0)
        0.0
    """
    try:
        value = getattr(obj, attr_name, None)
        if value is None and isinstance(obj, dict):
            value = obj.get(attr_name, None)
        if value is None:
            return default
        return transformer(value)
    except (AttributeError, TypeError, ValueError, KeyError):
        return default


def safe_or_raise(obj: Any, attr_name: str, error_message: str | None = None) -> Any:
    """
    Acesso a atributo com exceção clara se falhar.

    Args:
        obj: Objeto do qual acessar o atributo.
        attr_name: Nome do atributo.
        error_message: Mensagem de erro customizada.

    Returns:
        Valor do atributo.

    Raises:
        AttributeError: Se o atributo não existir.

    Examples:
        >>> class Config:
        ...     timeout = 30
        >>> config = Config()
        >>> safe_or_raise(config, "timeout")
        30
        >>> safe_or_raise(config, "missing")
        AttributeError: Attribute 'missing' not found on Config
    """
    if not hasattr(obj, attr_name):
        msg = error_message or f"Attribute '{attr_name}' not found on {obj.__class__.__name__}"
        raise AttributeError(msg)
    return getattr(obj, attr_name)
