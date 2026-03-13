from importlib import import_module
from pathlib import Path
import sys

from app.modules.educacao.core.domain import (
    AnoLetivo,
    CicloEnsino,
    Escola,
    InscricaoBasica,
    InscricaoSecundaria,
    InscricaoSuperior,
    InscricaoTecnico,
    Matricula,
    StatusMatricula,
    TipoEscola,
    Turma,
    Turno,
)

__all__ = [
    "AnoLetivo",
    "CicloEnsino",
    "Escola",
    "InscricaoBasica",
    "InscricaoSecundaria",
    "InscricaoSuperior",
    "InscricaoTecnico",
    "Matricula",
    "StatusMatricula",
    "TipoEscola",
    "Turma",
    "Turno",
]

# Allow legacy imports like app.modules.educacao.domain.models.<module>
# to resolve against the core domain module files.
_core_domain_path = Path(__file__).resolve().parents[2] / "core" / "domain"
if str(_core_domain_path) not in __path__:
    __path__.append(str(_core_domain_path))

_SUBMODULES = [
    "_workflow_record",
    "ano_letivo",
    "escola",
    "matricula",
    "turma",
    "inscricao_basica",
    "inscricao_secundaria",
    "inscricao_superior",
    "inscricao_tecnico",
]

for _mod in _SUBMODULES:
    sys.modules[f"{__name__}.{_mod}"] = import_module(
        f"app.modules.educacao.core.domain.{_mod}"
    )
