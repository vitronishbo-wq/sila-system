from __future__ import annotations


try:
    from apps.backend.app.modules.educacao.domain.ano_letivo import AnoLetivo  # type: ignore
except Exception:
    class AnoLetivo:  # Fallback shim for import compatibility
        pass
