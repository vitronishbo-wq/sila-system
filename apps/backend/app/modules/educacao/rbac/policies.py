from __future__ import annotations

from typing import Optional

from sila_platform.governance.rbac.policies import (
    get_permissions as gov_get_permissions,
    check_permission as gov_check_permission,
)
from apps.backend.app.modules.educacao.rbac.roles import (
    RoleMinisterial,
    role_inferiores,
    _to_gov,
)

# Permissões específicas da Educação (complementares às da governance)
_EDUCACAO_PERMISSION_MAP: dict[str, set[str]] = {
    "ministerio": {
        "criar_politicas",
        "criar_calendario_nacional",
        "criar_tipos_escola",
        "monitorizar_emis",
        "ver_indicadores_nacionais",
        "aprovar_integracoes",
        "gerir_administracao_central",
        "auditar_todas_provincias",
        "delegar_para_provincia",
    },
    "provincia": {
        "ver_apenas_sua_provincia",
        "validar_escolas",
        "gerir_vagas_provinciais",
        "emitir_relatorios_provinciais",
        "auditar_municipios",
        "delegar_para_municipio",
    },
    "municipio": {
        "ver_apenas_seu_municipio",
        "transferencias_locais",
        "monitorar_matriculas",
        "fiscalizar_escolas",
        "confirmar_matriculas",
        "delegar_para_escola",
    },
    "escola": {
        "aceitar_matricula",
        "emitir_declaracao",
        "emitir_certificado",
        "gerir_turmas",
        "gerir_professores",
        "validar_matriculas",
        "visualizar_alunos",
    },
    "operador": {
        "consultar_estudante",
        "atualizar_dados",
        "submeter_documentos",
    },
}


def _get_educacao_permissions(role: RoleMinisterial) -> set[str]:
    base = _EDUCACAO_PERMISSION_MAP.get(role.value, set()).copy()
    for inferior_role in role_inferiores(role):
        base |= _EDUCACAO_PERMISSION_MAP.get(inferior_role.value, set())
    return base


def get_permissions(role: RoleMinisterial) -> set[str]:
    """Permissões da Educação + permissões herdadas da governance."""
    gov_perms = gov_get_permissions(_to_gov(role))
    edu_perms = _get_educacao_permissions(role)
    return gov_perms | edu_perms


def get_role_permissions(role_value: str) -> set[str]:
    try:
        role = RoleMinisterial(role_value)
    except ValueError:
        return set()
    return get_permissions(role)


def check_permission(role: RoleMinisterial, permission: str) -> bool:
    return permission in get_permissions(role)
