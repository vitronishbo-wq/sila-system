"""
Base abstract class for request services across all modules.

This module provides a foundational abstraction that consolidates common
request lifecycle patterns (create, retrieve, list, update, notify, audit)
across different domains (citizen requests, service requests, healthcare, etc.).

The BaseRequestService uses the Template Method pattern to define the skeleton
of request operations, allowing subclasses to customize specific steps without
breaking the overall workflow structure.

Architecture:
- BaseRequestService: Abstract base with template methods + shared utilities
- Concrete services: Inherit and override domain-specific methods
- Repository pattern: Injected as dependency for data access
- Notification service: Optional, injected for cross-cutting concerns
- Audit logging: Automatic, centralized in base class
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from uuid import UUID

from apps.backend.app.core.audit import audit_log
from sqlalchemy.ext.asyncio import AsyncSession

TRequest = TypeVar("TRequest")
TRepository = TypeVar("TRepository")


class BaseRequestService(ABC, Generic[TRequest, TRepository]):
    """
    Abstract base class for request services across all business domains.

    Provides:
    - Common CRUD patterns (async/await)
    - Audit trail integration
    - Notification hooks
    - Permission validation framework
    - Status transition handling

    Subclasses must implement:
    - get_repository(): Return domain-specific repository
    - default_status(): Define initial status for new requests
    - create_request_model(): Instantiate domain request entity
    - get_user_from_citizen_id(): Map citizen_id to user for notifications
    """

    def __init__(
        self,
        db: AsyncSession,
        repository: TRepository | None = None,
        notification_service: Any | None = None,
        audit_enabled: bool = True,
        **kwargs,
    ):
        """
        Initialize base request service.

        Args:
            db: AsyncSession for database operations
            repository: Optional pre-configured repository (if None, get_repository() is called)
            notification_service: Optional notification service for async notifications
            audit_enabled: Whether to log audit trail (default: True)
            **kwargs: Additional domain-specific dependencies
        """
        self.db = db
        self.repo = repository or self.get_repository()
        self.notification_svc = notification_service
        self.audit_enabled = audit_enabled
        for k, v in kwargs.items():
            setattr(self, k, v)

    @abstractmethod
    def get_repository(self) -> TRepository:
        """
        Return the repository instance for this service.

        Subclasses must implement to return domain-specific repository.
        Called in __init__ if no repository passed.

        Example:
            def get_repository(self):
                return RequestRepository(self.db)
        """
        pass

    @abstractmethod
    def default_status(self) -> str:
        """
        Define the initial status for newly created requests.

        Must be valid for domain (e.g., "PENDING", "DRAFT", "SUBMITTED").

        Returns:
            str: Status value as string
        """
        pass

    @abstractmethod
    async def create_request_model(
        self, citizen_id: UUID, request_data: dict[str, Any], **kwargs
    ) -> TRequest:
        """
        Factory method to create domain-specific request entity.

        Called by create_request() to instantiate the appropriate model.

        Args:
            citizen_id: Citizen UUID
            request_data: Creating user's request payload
            **kwargs: Domain-specific parameters

        Returns:
            TRequest: Instantiated request model (not yet saved)
        """
        pass

    @abstractmethod
    async def get_user_from_citizen_id(self, citizen_id: UUID) -> UUID | None:
        """
        Resolve citizen_id to user_id for notification routing.

        Args:
            citizen_id: Citizen UUID

        Returns:
            Optional[UUID]: User ID if found, None otherwise
        """
        pass

    async def create_request(
        self, citizen_id: UUID, created_by: UUID, request_data: dict[str, Any], **kwargs
    ) -> TRequest:
        """
        Template method: Create new request.

        Workflow:
        1. Validate input (can be overridden)
        2. Create request model
        3. Pre-save hook (can be overridden)
        4. Save to repository
        5. Post-save hook (can be overridden)
        6. Audit log

        Args:
            citizen_id: Citizen UUID
            created_by: User UUID who created request
            request_data: Request payload
            **kwargs: Domain-specific parameters

        Returns:
            TRequest: Saved request entity
        """
        await self._validate_create_request(citizen_id, request_data, **kwargs)
        request = await self.create_request_model(citizen_id, request_data, **kwargs)
        await self._pre_save_create(request)
        saved = await self.repo.save(request)
        await self._post_save_create(saved, created_by)
        if self.audit_enabled:
            await self._audit_create(saved, created_by)
        return saved

    async def get_request(
        self, request_id: UUID, user_id: UUID, is_citizen: bool = False, **kwargs
    ) -> TRequest | None:
        """
        Template method: Retrieve single request with permission check.

        Workflow:
        1. Fetch from repository
        2. Permission check (overridable)
        3. Return (or None if no permission)

        Args:
            request_id: Request UUID
            user_id: Requesting user UUID
            is_citizen: Whether requester is citizen (for permission logic)
            **kwargs: Domain-specific parameters

        Returns:
            Optional[TRequest]: Request if accessible, None otherwise
        """
        request = await self.repo.get_by_id(request_id)
        if not request:
            return None
        if not await self._check_read_permission(request, user_id, is_citizen, **kwargs):
            return None
        return request

    async def list_requests(
        self, skip: int = 0, limit: int = 100, citizen_id: UUID | None = None, **filters
    ) -> tuple[list[TRequest], int]:
        """
        Template method: List requests with optional citizen filter.

        Args:
            skip: Pagination offset
            limit: Pagination limit
            citizen_id: Optional Citizen UUID to filter by
            **filters: Domain-specific filters (status, channel, etc.)

        Returns:
            Tuple: (List[TRequest], total_count)
        """
        if citizen_id:
            return await self.repo.get_by_citizen(citizen_id, skip, limit, **filters)
        if hasattr(self.repo, "list_all"):
            return await self.repo.list_all(skip, limit, **filters)
        if hasattr(self.repo, "search"):
            return await self.repo.search(query="", filters=filters, skip=skip, limit=limit)
        return ([], 0)

    async def get_request_status(self, request_id: UUID) -> str | None:
        """
        Get current status of a request.

        Useful for lightweight status checks without fetching full request.

        Args:
            request_id: Request UUID

        Returns:
            Optional[str]: Status value or None if not found
        """
        request = await self.repo.get_by_id(request_id)
        return request.status if request else None

    async def _validate_create_request(
        self, citizen_id: UUID, request_data: dict[str, Any], **kwargs
    ) -> None:
        """
        Validate create request input.

        Override in subclass to add domain validations.
        Raise exception if validation fails (e.g., ValueError, ValidationError).

        Default: No validation (pass)

        Args:
            citizen_id: Citizen UUID
            request_data: Request payload
            **kwargs: Domain-specific parameters

        Raises:
            ValueError: If validation fails
        """
        pass

    async def _pre_save_create(self, request: TRequest) -> None:
        """
        Hook before saving new request to database.

        Override to normalize/transform request model before persistence.

        Default: No action (pass)

        Args:
            request: Unsaved request model (can modify in place)
        """
        pass

    async def _post_save_create(self, saved_request: TRequest, created_by: UUID) -> None:
        """
        Hook after saving new request to database.
        """
        if self.notification_svc:
            try:
                user_id = await self.get_user_from_citizen_id(saved_request.citizen_id)
                if user_id:
                    await self.notification_svc.notify_request_created(
                        user_id=user_id,
                        request_id=saved_request.id,
                        request_data={"status": saved_request.status},
                    )
            except Exception as e:
                print(f"Warning: Notification failed for request {saved_request.id}: {e}")

    async def _post_status_change(
        self, request: TRequest, old_status: str, new_status: str, updated_by: UUID
    ) -> None:
        """
        Hook after status update. Triggers notifications by default.
        """
        if self.notification_svc:
            try:
                user_id = await self.get_user_from_citizen_id(request.citizen_id)
                if user_id:
                    await self.notification_svc.notify_request_status_changed(
                        user_id=user_id,
                        request_id=request.id,
                        old_status=old_status,
                        new_status=new_status,
                    )
            except Exception as e:
                print(f"Warning: Status notification failed for request {request.id}: {e}")

    async def _check_read_permission(
        self, request: TRequest, user_id: UUID, is_citizen: bool = False, **kwargs
    ) -> bool:
        """
        Check if user has permission to read request.

        Override in subclass to implement domain-specific permission logic.

        Default: Citizens can only read own requests

        Args:
            request: Request entity to check
            user_id: Requesting user UUID
            is_citizen: Is requester a citizen?
            **kwargs: Domain-specific parameters (roles, etc.)

        Returns:
            bool: True if access allowed, False otherwise
        """
        if is_citizen:
            return hasattr(request, "citizen_id") and request.citizen_id == user_id
        return True

    async def _audit_create(self, saved_request: TRequest, created_by: UUID) -> None:
        """
        Log creation to audit trail.

        Override in subclass for custom audit fields.

        Default: Uses centralized audit_log utility

        Args:
            saved_request: Saved request entity
            created_by: User UUID who created request
        """
        await audit_log(
            action="REQUEST_CREATED",
            actor_id=str(created_by),
            resource_id=str(saved_request.id),
            resource_type=self.__class__.__name__,
            new_value={
                "citizen_id": str(saved_request.citizen_id)
                if hasattr(saved_request, "citizen_id")
                else None,
                "status": saved_request.status if hasattr(saved_request, "status") else None,
            },
            db=self.db,
        )

    async def update_status(
        self,
        request_id: UUID,
        new_status: str,
        updated_by: UUID,
        reason: str | None = None,
        **kwargs,
    ) -> TRequest | None:
        """
        Update request status with audit trail.

        Args:
            request_id: Request UUID
            new_status: New status value
            updated_by: User UUID performing update
            reason: Optional reason for status change
            **kwargs: Domain-specific parameters

        Returns:
            Optional[TRequest]: Updated request or None if not found
        """
        request = await self.repo.get_by_id(request_id)
        if not request:
            return None
        old_status = request.status if hasattr(request, "status") else None
        request.status = new_status
        updated = await self.repo.save(request)
        await self._post_status_change(updated, str(old_status), str(new_status), updated_by)
        if self.audit_enabled:
            await audit_log(
                action="REQUEST_STATUS_UPDATED",
                actor_id=str(updated_by),
                resource_id=str(request_id),
                resource_type=self.__class__.__name__,
                old_value={"status": str(old_status)},
                new_value={"status": str(new_status)},
                metadata={"reason": reason} if reason else {},
                db=self.db,
            )
        return updated

    async def count_by_citizen(self, citizen_id: UUID) -> int:
        """
        Count total requests for a citizen.

        Args:
            citizen_id: Citizen UUID

        Returns:
            int: Total count
        """
        _, total = await self.repo.get_by_citizen(citizen_id, skip=0, limit=1)
        return total


class BaseRequestServiceSync(ABC):
    """
    Synchronous variant of BaseRequestService for legacy services.

    Use this if your repository/service is synchronous (blocking I/O).
    Mirrors BaseRequestService interface but without async/await.

    Not recommended for new code; use BaseRequestService for async.
    """

    def __init__(
        self,
        repository: TRepository,
        notification_service: Any | None = None,
        audit_enabled: bool = True,
        **kwargs,
    ):
        """
        Initialize sync request service.

        Args:
            repository: Pre-configured sync repository
            notification_service: Optional notification service
            audit_enabled: Whether to log audit trail
            **kwargs: Additional domain-specific dependencies
        """
        self.repo = repository
        self.notification_svc = notification_service
        self.audit_enabled = audit_enabled
        for k, v in kwargs.items():
            setattr(self, k, v)

    @abstractmethod
    def default_status(self) -> str:
        """Define initial request status."""
        pass

    @abstractmethod
    def create_request_model(
        self, citizen_id: UUID, request_data: dict[str, Any], **kwargs
    ) -> TRequest:
        """Factory method for domain-specific request entity."""
        pass
