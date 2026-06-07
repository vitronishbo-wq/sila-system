"""
SILA Core Context Variables - Correlação de Requisições

Fornece um sistema thread-safe de variáveis de contexto que flutua
através de toda a pilha assíncrona sem necessidade de passar manualmente.

Uso:
    from apps.backend.app.core.observability.context import get_request_id, set_request_context

    # No middleware
    set_request_context(
        request_id="123e-4567-89ab-cdef",
        user_id="user_456",
        territory_id="province_luanda"
    )

    # Em qualquer lugar da stack assíncrona
    request_id = get_request_id()  # "123e-4567-89ab-cdef"
"""

import contextvars
import uuid
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

_request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default=None)
_user_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("user_id", default=None)
_tenant_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "tenant_id", default=None
)
_territory_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "territory_id", default=None
)
_user_roles_var: contextvars.ContextVar[tuple[str, ...]] = contextvars.ContextVar(
    "user_roles", default=()
)
_service_name_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "service_name", default=None
)
_trace_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("trace_id", default=None)
_span_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar("span_id", default=None)
_start_time_var: contextvars.ContextVar[datetime | None] = contextvars.ContextVar(
    "start_time", default=None
)


def generate_request_id() -> str:
    """Gera um novo request_id único (UUID v4 comprimido)."""
    return str(uuid.uuid4())


def set_request_context(
    request_id: str | None = None,
    user_id: str | None = None,
    tenant_id: str | None = None,
    territory_id: str | None = None,
    service_name: str | None = None,
    trace_id: str | None = None,
    span_id: str | None = None,
    user_roles: Iterable[str] | None = None,
) -> str:
    """
    Configura o contexto da requisição.

    Args:
        request_id: ID único da requisição (gerado se não fornecido)
        user_id: ID do usuário autenticado
        territory_id: ID territorial (province, district, etc)
        service_name: Nome do serviço que processa
        trace_id: ID de rastreamento distribuído (OpenTelemetry)
        span_id: ID de span distribuído (OpenTelemetry)

    Returns:
        O request_id (gerado ou fornecido)
    """
    if not request_id:
        request_id = generate_request_id()
    _request_id_var.set(request_id)
    _user_id_var.set(user_id)
    resolved_tenant = tenant_id or territory_id
    _tenant_id_var.set(resolved_tenant)
    _territory_id_var.set(territory_id or resolved_tenant)
    _service_name_var.set(service_name)
    _trace_id_var.set(trace_id or request_id)
    _span_id_var.set(span_id)
    _start_time_var.set(datetime.now(UTC))
    if user_roles is not None:
        _user_roles_var.set(tuple(user_roles))
    return request_id


def set_security_context(
    user_id: str | None = None,
    tenant_id: str | None = None,
    roles: Iterable[str] | None = None,
    request_id: str | None = None,
) -> str:
    """
    Atualiza apenas os aspectos de segurança (user/tenant/roles) do contexto
    sem sobrescrever outros campos já definidos.

    Args:
        user_id: Identificador do usuário autenticado
        tenant_id: Identificador do tenant / domínio
        roles: Coleção de roles do usuário
        request_id: Request id atual (gera se ausente)

    Returns:
        request_id efetivo em uso
    """
    current_request = _request_id_var.get() or request_id or generate_request_id()
    _request_id_var.set(current_request)
    if user_id is not None:
        _user_id_var.set(user_id)
    if tenant_id is not None:
        _tenant_id_var.set(tenant_id)
    if tenant_id is not None and _territory_id_var.get() is None:
        _territory_id_var.set(tenant_id)
    if roles is not None:
        _user_roles_var.set(tuple(roles))
    if _start_time_var.get() is None:
        _start_time_var.set(datetime.now(UTC))
    return current_request


def get_request_id() -> str:
    """Obtém o request_id atual (gera se não existir)."""
    request_id = _request_id_var.get()
    if not request_id:
        request_id = set_request_context()
    return request_id


def get_user_id() -> str | None:
    """Obtém o user_id do contexto."""
    return _user_id_var.get()


def get_territory_id() -> str | None:
    """Obtém o territory_id do contexto."""
    return _territory_id_var.get()


def get_tenant_id() -> str | None:
    """Obtém o tenant_id do contexto (separado de território)."""
    return _tenant_id_var.get()


def get_user_roles() -> tuple[str, ...]:
    """Obtém roles do usuário atuais."""
    return _user_roles_var.get()


def get_service_name() -> str | None:
    """Obtém o service_name do contexto."""
    return _service_name_var.get()


def get_trace_id() -> str | None:
    """Obtém o trace_id (para OpenTelemetry)."""
    return _trace_id_var.get()


def get_span_id() -> str | None:
    """Obtém o span_id (para OpenTelemetry)."""
    return _span_id_var.get()


def get_start_time() -> datetime | None:
    """Obtém o tempo de início da requisição."""
    return _start_time_var.get()


def get_duration_ms() -> float:
    """Calcula a duração da requisição em milissegundos."""
    start_time = get_start_time()
    if not start_time:
        return 0.0
    duration = datetime.now(UTC) - start_time
    return duration.total_seconds() * 1000


def get_context_dict() -> dict[str, Any]:
    """
    Obtém o dicionário completo do contexto.
    Útil para logs estruturados e tracing distribuído.

    Returns:
        Dict com todos os valores de contexto
    """
    return {
        "request_id": get_request_id(),
        "user_id": get_user_id(),
        "tenant_id": get_tenant_id(),
        "territory_id": get_territory_id(),
        "user_roles": list(get_user_roles() or ()),
        "service_name": get_service_name(),
        "trace_id": get_trace_id(),
        "span_id": get_span_id(),
        "duration_ms": get_duration_ms(),
    }


def clear_context():
    """Limpa o contexto (útil em testes)."""
    _request_id_var.set(None)
    _user_id_var.set(None)
    _tenant_id_var.set(None)
    _territory_id_var.set(None)
    _user_roles_var.set(())
    _service_name_var.set(None)
    _trace_id_var.set(None)
    _span_id_var.set(None)
    _start_time_var.set(None)


__all__ = [
    "generate_request_id",
    "set_request_context",
    "set_security_context",
    "get_request_id",
    "get_user_id",
    "get_tenant_id",
    "get_territory_id",
    "get_user_roles",
    "get_service_name",
    "get_trace_id",
    "get_span_id",
    "get_start_time",
    "get_duration_ms",
    "get_context_dict",
    "clear_context",
]
