import sys
from importlib import import_module
from pathlib import Path

try:
    from apps.backend.app.modules.educacao.domain.ano_letivo import AnoLetivo
    from apps.backend.app.modules.educacao.domain.escola import CicloEnsino, Escola, TipoEscola
    from apps.backend.app.modules.educacao.domain.inscricao_basica import InscricaoBasica
    from apps.backend.app.modules.educacao.domain.inscricao_secundaria import InscricaoSecundaria
    from apps.backend.app.modules.educacao.domain.inscricao_superior import InscricaoSuperior
    from apps.backend.app.modules.educacao.domain.inscricao_tecnico import InscricaoTecnico
    from apps.backend.app.modules.educacao.domain.matricula import Matricula, StatusMatricula
    from apps.backend.app.modules.educacao.domain.turma import Turma, Turno
except ImportError:
    pass
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
    try:
        module = import_module(f"apps.backend.app.modules.educacao.domain.{_mod}")
    except ModuleNotFoundError:
        module = import_module(f"apps.backend.app.modules.educacao.domain.{_mod}")
    sys.modules[f"{__name__}.{_mod}"] = module
