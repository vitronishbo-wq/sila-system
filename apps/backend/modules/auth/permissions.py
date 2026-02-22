# modules/auth/permissions.py
from enum import StrEnum
from functools import wraps
from typing import Callable, TypeVar

from fastapi import HTTPException, status

# Usamos StrEnum (Python 3.11+) para melhor compatibilidade e herança de str
class AccessLevel(StrEnum):
    local = "local"
    provincial = "provincial"
    central = "central"


# Ordem hierárquica para comparação
LEVEL_ORDER = {
    AccessLevel.local: 1,
    AccessLevel.provincial: 2,
    AccessLevel.central: 3,
}

F = TypeVar("F", bound=Callable)


def requires_level(min_level: AccessLevel) -> Callable[[F], F]:
    """
    Decorador para endpoints que verifica o nível de acesso do usuário.
    Espera que o usuário (passado como dependência) tenha um atributo `level`.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Autenticação necessária",
                )

            user_level = getattr(user, "level", None)
            if user_level not in LEVEL_ORDER:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Nível de acesso inválido",
                )

            if LEVEL_ORDER[user_level] < LEVEL_ORDER[min_level]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Acesso negado: nível insuficiente",
                )

            return func(user, *args, **kwargs)

        return wrapper

    return decorator