from unittest.mock import AsyncMock, patch

import pytest

from foundation.resilience.idempotency import (
    DuplicateRequestError,
    IdempotencyKeyMissingError,
    InMemoryIdempotencyStore,
    RedisIdempotencyStore,
    extract_idempotency_key,
    idempotent,
)


def test_extract_idempotency_key_from_headers() -> None:
    headers = {"Idempotency-Key": "abc123"}
    assert extract_idempotency_key(headers) == "abc123"


def test_idempotent_decorator_requires_key() -> None:
    store = InMemoryIdempotencyStore()

    @idempotent(operation_name="payment.create", store=store)
    def create_payment(amount: int, idempotency_key: str | None = None) -> int:
        return amount * 2

    with pytest.raises(IdempotencyKeyMissingError):
        create_payment(10)


def test_idempotent_decorator_blocks_duplicate_requests() -> None:
    store = InMemoryIdempotencyStore()

    @idempotent(operation_name="enrollment.create", store=store)
    def create_enrollment(student_id: str, idempotency_key: str | None = None) -> dict[str, str]:
        return {"student_id": student_id, "status": "created"}

    result = create_enrollment("student-1", idempotency_key="key-123")
    assert result["status"] == "created"

    with pytest.raises(DuplicateRequestError):
        create_enrollment("student-1", idempotency_key="key-123")


@pytest.mark.asyncio
async def test_idempotent_decorator_async_operation() -> None:
    store = InMemoryIdempotencyStore()

    @idempotent(operation_name="transfer.execute", store=store)
    async def execute_transfer(student_id: str, idempotency_key: str | None = None) -> str:
        return f"transferred:{student_id}"

    result = await execute_transfer("student-2", idempotency_key="key-456")
    assert result == "transferred:student-2"

    with pytest.raises(DuplicateRequestError):
        await execute_transfer("student-2", idempotency_key="key-456")


@pytest.mark.asyncio
async def test_redis_idempotency_store_serializes_values_and_checks_exists() -> None:
    fake_client = AsyncMock()
    fake_client.get.return_value = '{"completed": true, "result": "ok"}'
    fake_client.exists.return_value = 1
    fake_client.setex = AsyncMock()
    fake_client.set = AsyncMock()
    fake_client.delete = AsyncMock()

    store = RedisIdempotencyStore(fake_client)

    assert store._client is fake_client

    result = await store.get("test-key")
    assert result == {"completed": True, "result": "ok"}

    await store.set("test-key", {"completed": True, "result": "ok"}, ttl_seconds=30)
    fake_client.setex.assert_awaited_once()

    exists = await store.exists("test-key")
    assert exists is True

    await store.delete("test-key")
    fake_client.delete.assert_awaited_once_with("test-key")
