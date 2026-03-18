from __future__ import annotations

from typing import Iterable, Optional, Tuple
from fastapi import APIRouter


class HealthRouterFactory:
    """Factory for creating standardized health routers."""

    @staticmethod
    def infer_module_name(
        module_path: str,
        infer_indices: Tuple[int, int] = (3, 4),
        separator: str = ".",
    ) -> str:
        parts = module_path.split(".")
        try:
            left, right = infer_indices
            return f"{parts[left]}{separator}{parts[right]}"
        except Exception:
            return module_path

    @staticmethod
    def create_health_router(
        *,
        status_value: str = "ok",
        module_name: Optional[str] = None,
        include_module: bool = True,
        tags: Optional[list[str]] = None,
        path: str = "/health",
    ) -> APIRouter:
        router = APIRouter()

        @router.get(path, tags=tags)
        def health() -> dict:
            payload: dict = {"status": status_value}
            if include_module and module_name:
                payload["module"] = module_name
            return payload

        return router

    @classmethod
    def create_inferred_health_router(
        cls,
        *,
        module_path: str,
        infer_indices: Tuple[int, int] = (3, 4),
        status_value: str = "ok",
        tags: Optional[list[str]] = None,
        path: str = "/health",
    ) -> APIRouter:
        module_name = cls.infer_module_name(module_path, infer_indices=infer_indices)
        return cls.create_health_router(
            status_value=status_value,
            module_name=module_name,
            include_module=True,
            tags=tags,
            path=path,
        )


__all__ = ["HealthRouterFactory"]
