# Presentation layer API package (compat shims)
from ...application.api.citizens import citizens_routes  # type: ignore
from ...application.api.documents import documents_routes  # type: ignore

__all__ = ["citizens_routes", "documents_routes"]
