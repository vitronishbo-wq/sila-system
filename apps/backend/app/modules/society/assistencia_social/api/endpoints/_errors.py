from __future__ import annotations

from fastapi import HTTPException, status


def raise_http_for_value_error(exc: ValueError) -> None:
    message = str(exc)
    if "nao encontrado" in message.lower():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
