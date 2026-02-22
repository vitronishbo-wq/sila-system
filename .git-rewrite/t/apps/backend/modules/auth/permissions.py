from enum import Enum
from functools import wraps
from typing import Callable

from fastapi import HTTPException, status


class AccessLevel(str, Enum):
    local = "local"
    provincial = "provincial"
    central = "central"


LEVEL_ORDER = {
    AccessLevel.local: 1,
    AccessLevel.provincial: 2,
    AccessLevel.central: 3,
}


def requires_level(min_level: AccessLevel) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            user_level = getattr(user, "level", None)
            if (
                user_level is None
                or LEVEL_ORDER.get(user_level, 0) < LEVEL_ORDER[min_level]
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado"
                )
            return func(user, *args, **kwargs)

        return wrapper

    return decorator


# auto-generated placeholder
