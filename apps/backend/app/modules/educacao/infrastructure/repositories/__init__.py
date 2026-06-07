"""Lazy-loading exports for educacao repositories to avoid circular imports."""

from __future__ import annotations

import importlib
import re
from typing import Any

__all__ = [
    "SQLAlchemyAcademicIdentityRepository",
    "SQLAlchemyEnrollmentRepository",
    "SQLAlchemyCapacityRepository",
    "SQLAlchemyTransferRepository",
    "SQLAlchemyMatriculaRepository",
    "SQLAlchemyTurmaRepository",
    "SQLAlchemyEscolaRepository",
    "SQLAlchemyInscricaoRepository",
    "SQLAlchemyBoletimRepository",
    "SQLAlchemyCertificadoRepository",
    "SQLAlchemyTransferenciaRepository",
    "SQLAlchemyPropinaRepository",
    "SQLAlchemyEmpregoRepository",
    "SQLAlchemyConcursoRepository",
    "SQLAlchemyFormacaoRepository",
    "SQLAlchemyUniversidadeRepository",
    "SQLAlchemyGuardianRepository",
]


def _camel_to_snake(name: str) -> str:
    # Special-case SQLAlchemy-prefixed classes (SQLAlchemyFoo -> sqlalchemy_foo)
    if name.startswith("SQLAlchemy"):
        remainder = name[len("SQLAlchemy") :]
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", remainder)
        snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
        return f"sqlalchemy_{snake}"
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def __getattr__(name: str) -> Any:  # module-level lazy import
    if name not in __all__:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name = _camel_to_snake(name)
    module = importlib.import_module(f".{module_name}", __name__)
    return getattr(module, name)


def __dir__():
    return sorted(list(__all__))
