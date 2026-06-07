from __future__ import annotations

from sila_platform.governance.rbac.roles import RoleGovernance, role_inferiores


_PERMISSION_MAP: dict[str, set[str]] = {
    "nacional": {
        "criar_politicas",
        "criar_calendario_nacional",
        "criar_tipos_unidade",
        "monitorizar_emis",
        "ver_indicadores_nacionais",
        "aprovar_integracoes",
        "gerir_administracao_central",
        "auditar_todas_provincias",
        "delegar_para_provincia",
    },
    "provincial": {
        "ver_apenas_sua_provincia",
        "validar_unidades",
        "gerir_vagas_provinciais",
        "emitir_relatorios_provinciais",
        "auditar_municipios",
        "delegar_para_municipio",
    },
    "municipal": {
        "ver_apenas_seu_municipio",
        "transferencias_locais",
        "monitorar_atividades",
        "fiscalizar_unidades",
        "confirmar_registros",
        "delegar_para_unidade",
    },
    "unidade": {
        "aceitar_registro",
        "emitir_declaracao",
        "emitir_certificado",
        "gerir_turmas",
        "gerir_profissionais",
        "validar_registros",
        "visualizar_utentes",
    },
    "operador": {
        "consultar_registro",
        "atualizar_dados",
        "submeter_documentos",
    },
}


def _inherit_permissions(role: RoleGovernance) -> set[str]:
    base = _PERMISSION_MAP.get(role.value, set()).copy()
    for inferior_role in role_inferiores(role):
        base |= _PERMISSION_MAP.get(inferior_role.value, set())
    return base


def get_permissions(role: RoleGovernance) -> set[str]:
    return _inherit_permissions(role)


def get_role_permissions(role_value: str) -> set[str]:
    try:
        role = RoleGovernance(role_value)
    except ValueError:
        return set()
    return get_permissions(role)


def check_permission(role: RoleGovernance, permission: str) -> bool:
    return permission in _inherit_permissions(role)
