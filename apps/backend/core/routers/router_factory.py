"""
RouterFactory - Generate FastAPI router classes
Consolidates 28 routers.py files (P1 Phase)

Pattern:
  create_module_router(module_name, prefix) -> APIRouter
  with automatic endpoint registration
"""

from typing import Any

from fastapi import APIRouter


class RouterFactory:
    """Factory for generating FastAPI router instances"""

    @staticmethod
    def create_module_router(
        module_name: str, prefix: str = None, tags: list[str] = None, include_crud: bool = True
    ) -> APIRouter:
        """
        Create a standardized FastAPI router for a module.

        Args:
            module_name: Name of the module (e.g., 'Documents', 'Payment')
            prefix: URL prefix for routes (e.g., '/documents')
            tags: OpenAPI tags for documentation
            include_crud: Whether to include standard CRUD endpoints

        Returns:
            Configured FastAPI APIRouter instance
        """

        if prefix is None:
            prefix = f"/{module_name.lower()}"

        if tags is None:
            tags = [module_name]

        router = APIRouter(prefix=prefix, tags=tags)

        # Health check endpoint
        @router.get("/health", tags=["health"])
        async def health_check():
            """Health check endpoint for the module"""
            return {"status": "healthy", "module": module_name, "version": "1.0.0"}

        # Standard CRUD helpers (customizable in module)
        if include_crud:

            @router.get("/", tags=tags)
            async def list_items():
                """List all items in the module"""
                return {"module": module_name, "items": []}

            @router.post("/", tags=tags)
            async def create_item(item: dict[str, Any]):
                """Create a new item in the module"""
                return {"id": 1, "module": module_name, "item": item}

            @router.get("/{item_id}", tags=tags)
            async def read_item(item_id: int):
                """Read a specific item by ID"""
                return {"id": item_id, "module": module_name}

            @router.put("/{item_id}", tags=tags)
            async def update_item(item_id: int, item: dict[str, Any]):
                """Update an item"""
                return {"id": item_id, "module": module_name, "updated": item}

            @router.delete("/{item_id}", tags=tags)
            async def delete_item(item_id: int):
                """Delete an item"""
                return {"id": item_id, "module": module_name, "deleted": True}

        return router

    @staticmethod
    def create_composite_router(
        main_router_name: str, sub_routers: dict[str, APIRouter], prefix: str = None
    ) -> APIRouter:
        """
        Create a composite router from multiple sub-routers.

        Args:
            main_router_name: Name of the main router
            sub_routers: Dictionary of {name: router} to include
            prefix: Optional main prefix

        Returns:
            Composite APIRouter with all sub-routers included
        """

        if prefix is None:
            prefix = f"/{main_router_name.lower()}"

        main_router = APIRouter(prefix=prefix, tags=[main_router_name])

        # Include sub-routers
        for _name, sub_router in sub_routers.items():
            main_router.include_router(sub_router)

        return main_router

    @staticmethod
    def create_health_only_router(
        prefix: str,
        tags: list[str] | None = None,
        health_router: APIRouter | None = None,
    ) -> APIRouter:
        """
        Create a simple module router that only includes a health router.
        """
        if tags is None:
            tags = ["endpoints"]

        router = APIRouter(prefix=prefix, tags=tags)

        if health_router is not None:
            router.include_router(health_router)

        return router


__all__ = ["RouterFactory"]
