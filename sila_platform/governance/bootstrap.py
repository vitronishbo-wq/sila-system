from __future__ import annotations

"""Bootstrap da Governança — regista módulos, organizações e tenants.

Uso:
    from sila_platform.governance.bootstrap import bootstrap_governance
    registry, orgs, tenants = bootstrap_governance()
"""

from sila_platform.governance.organization.models import (
    Organization,
    OrganizationTree,
    OrganizationType,
)
from sila_platform.governance.registry.catalog import (
    ModuleRegistry,
    ModuleStatus,
    RegistryCatalog,
    TerritorialModel,
)
from sila_platform.governance.tenancy.models import Tenant, TenantManager, TenantStatus


def _build_educacao(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="mined", name="Ministério da Educação", org_type=OrganizationType.MINISTRY,
        module="educacao", code="MINED",
    ))
    orgs.register(Organization(
        id="dpe-huambo", name="Direção Provincial da Educação do Huambo",
        org_type=OrganizationType.PROVINCIAL_DIRECTORATE, module="educacao",
        parent_id="mined", province_id="huambo", province_name="Huambo",
    ))
    orgs.register(Organization(
        id="dme-caala", name="Direção Municipal da Educação da Caála",
        org_type=OrganizationType.MUNICIPAL_DIRECTORATE, module="educacao",
        parent_id="dpe-huambo", province_id="huambo", municipality_id="caala", municipality_name="Caála",
    ))
    registry.register(ModuleRegistry(
        module="educacao", name="Educação",
        description="Sistema Nacional de Gestão Educacional",
        owner_ministry="Ministério da Educação", owner_ministry_code="MINED",
        responsible_entity="Instituto Nacional de Educação",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_MUNICIPAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["escola", "municipio", "provincia"],
        enabled_services=["matricula", "transferencia", "certificado", "declaracao"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_MUNICIPIO", "ROLE_ESCOLA"],
        api_prefix="/api/v1/educacao",
        exposed_events=["student_enrolled", "student_transferred", "certificate_issued"],
        consumed_events=["citizen_updated", "identity_verified", "bi_issued"],
    ))


def _build_saude(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="minsa", name="Ministério da Saúde", org_type=OrganizationType.MINISTRY,
        module="saude", code="MINSA",
    ))
    orgs.register(Organization(
        id="dps-huambo", name="Direção Provincial da Saúde do Huambo",
        org_type=OrganizationType.PROVINCIAL_DIRECTORATE, module="saude",
        parent_id="minsa", province_id="huambo", province_name="Huambo",
    ))
    orgs.register(Organization(
        id="hospital-huambo", name="Hospital Geral do Huambo",
        org_type=OrganizationType.UNIT, module="saude",
        parent_id="dps-huambo", province_id="huambo", municipality_id="huambo",
        unit_id="hospital-huambo", unit_name="Hospital Geral do Huambo",
    ))
    registry.register(ModuleRegistry(
        module="saude", name="Saúde",
        description="Sistema Nacional de Gestão de Saúde",
        owner_ministry="Ministério da Saúde", owner_ministry_code="MINSA",
        responsible_entity="Direção Nacional de Saúde",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["unidade", "municipio", "provincia"],
        enabled_services=["marcacao_consulta", "receituario", "referenciacao", "internamento"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_MUNICIPIO", "ROLE_UNIDADE"],
        api_prefix="/api/v1/saude",
        exposed_events=["appointment_scheduled", "prescription_issued", "referral_made"],
        consumed_events=["citizen_updated", "identity_verified", "student_enrolled"],
    ))


def _build_justica(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="minjusdh", name="Ministério da Justiça e dos Direitos Humanos",
        org_type=OrganizationType.MINISTRY, module="justica", code="MINJUSDH",
    ))
    orgs.register(Organization(
        id="drh-huambo", name="Direção Regional da Justiça do Huambo",
        org_type=OrganizationType.PROVINCIAL_DIRECTORATE, module="justica",
        parent_id="minjusdh", province_id="huambo", province_name="Huambo",
    ))
    orgs.register(Organization(
        id="conservatoria-huambo", name="Conservatória do Registo Civil do Huambo",
        org_type=OrganizationType.UNIT, module="justica",
        parent_id="drh-huambo", province_id="huambo", municipality_id="huambo",
        unit_id="conservatoria-huambo", unit_name="Conservatória do Huambo",
    ))
    registry.register(ModuleRegistry(
        module="justica", name="Justiça",
        description="Sistema Nacional de Gestão da Justiça e Direitos Humanos",
        owner_ministry="Ministério da Justiça e dos Direitos Humanos",
        owner_ministry_code="MINJUSDH",
        responsible_entity="Direção Nacional da Justiça",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["unidade", "municipio", "provincia"],
        enabled_services=["registo_civil", "notariado", "tribunal", "criminal"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_MUNICIPIO", "ROLE_UNIDADE"],
        api_prefix="/api/v1/justica",
        exposed_events=["civil_registration_issued", "company_incorporated", "notarial_act_signed"],
        consumed_events=["citizen_updated", "identity_verified", "payment_confirmed"],
    ))


def _build_identity(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="minint", name="Ministério do Interior", org_type=OrganizationType.MINISTRY,
        module="identity", code="MININT",
    ))
    orgs.register(Organization(
        id="dni", name="Direção Nacional de Identificação",
        org_type=OrganizationType.PROVINCIAL_DIRECTORATE, module="identity",
        parent_id="minint",
    ))
    registry.register(ModuleRegistry(
        module="identity", name="Identificação Civil",
        description="Sistema Nacional de Identificação — BI, autenticação, verificação documental",
        owner_ministry="Ministério do Interior", owner_ministry_code="MININT",
        responsible_entity="Direção Nacional de Identificação",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["unidade", "municipio", "provincia"],
        enabled_services=["emitir_bi", "verificar_identidade", "autenticar_cidadao", "renovar_bi"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_MUNICIPIO", "ROLE_UNIDADE"],
        api_prefix="/api/v1/identity",
        exposed_events=["citizen_updated", "identity_verified", "bi_issued", "biometric_enrolled"],
        consumed_events=["birth_registered", "payment_confirmed", "death_registered"],
    ))


def _build_payment(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="minfin", name="Ministério das Finanças", org_type=OrganizationType.MINISTRY,
        module="payment", code="MINFIN",
    ))
    orgs.register(Organization(
        id="dntp", name="Direção Nacional do Tesouro Público",
        org_type=OrganizationType.PROVINCIAL_DIRECTORATE, module="payment",
        parent_id="minfin",
    ))
    registry.register(ModuleRegistry(
        module="payment", name="Pagamentos",
        description="Sistema Nacional de Pagamentos — taxas, propinas, multas e benefícios",
        owner_ministry="Ministério das Finanças", owner_ministry_code="MINFIN",
        responsible_entity="Direção Nacional do Tesouro Público",
        territorial_model=TerritorialModel.NACIONAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["unidade", "provincia"],
        enabled_services=["pagamento_taxas", "consultar_pagamento", "reembolso", "conciliacao"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_UNIDADE"],
        api_prefix="/api/v1/payment",
        exposed_events=["payment_confirmed", "payment_failed", "invoice_status_changed", "payment_reconciled"],
        consumed_events=["citizen_updated", "identity_verified", "student_enrolled", "nif_issued"],
    ))


def _build_registo_civil(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="minjusdh", name="Ministério da Justiça e dos Direitos Humanos",
        org_type=OrganizationType.MINISTRY, module="registo-civil", code="MINJUSDH",
    ))
    orgs.register(Organization(
        id="dnrc", name="Direção Nacional do Registo Civil",
        org_type=OrganizationType.PROVINCIAL_DIRECTORATE, module="registo-civil",
        parent_id="minjusdh",
    ))
    registry.register(ModuleRegistry(
        module="registo-civil", name="Registo Civil",
        description="Registos vitais: nascimento, casamento, óbito",
        owner_ministry="Ministério da Justiça e dos Direitos Humanos",
        owner_ministry_code="MINJUSDH",
        responsible_entity="Direção Nacional do Registo Civil",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_MUNICIPAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["unidade", "municipio", "provincia"],
        enabled_services=["registar_nascimento", "registar_casamento", "registar_obito", "consultar_registo"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_MUNICIPIO", "ROLE_UNIDADE"],
        api_prefix="/api/v1/registo-civil",
        exposed_events=["birth_registered", "marriage_registered", "death_registered"],
        consumed_events=["citizen_updated", "identity_verified"],
    ))


def _build_financas_impostos(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="minfin", name="Ministério das Finanças", org_type=OrganizationType.MINISTRY,
        module="financas-impostos", code="MINFIN",
    ))
    orgs.register(Organization(
        id="agt", name="Administração Geral Tributária",
        org_type=OrganizationType.PROVINCIAL_DIRECTORATE, module="financas-impostos",
        parent_id="minfin",
    ))
    registry.register(ModuleRegistry(
        module="financas-impostos", name="Finanças e Impostos",
        description="Gestão fiscal, tributação, NIF, declarações e cobrança",
        owner_ministry="Ministério das Finanças", owner_ministry_code="MINFIN",
        responsible_entity="Administração Geral Tributária",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["unidade", "provincia"],
        enabled_services=["emitir_nif", "declarar_impostos", "consultar_fiscal", "regularizar"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_UNIDADE"],
        api_prefix="/api/v1/financas-impostos",
        exposed_events=["nif_issued", "tax_declaration_submitted", "tax_payment_received"],
        consumed_events=["citizen_updated", "identity_verified", "company_incorporated", "payment_confirmed"],
    ))


def _build_administracao_local(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="mat", name="Ministério da Administração Territorial",
        org_type=OrganizationType.MINISTRY, module="administracao-local", code="MAT",
    ))
    registry.register(ModuleRegistry(
        module="administracao-local", name="Administração Local",
        description="Serviços municipais e provinciais — licenciamento, alvarás, atendimento",
        owner_ministry="Ministério da Administração Territorial",
        owner_ministry_code="MAT",
        responsible_entity="Direção Nacional da Administração Local",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_MUNICIPAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["municipio", "provincia"],
        enabled_services=["licenciamento", "alvara", "atestado_residencia", "atendimento_municipal"],
        required_roles=["ROLE_PROVINCIA", "ROLE_MUNICIPIO"],
        api_prefix="/api/v1/administracao-local",
        exposed_events=["license_issued", "residence_confirmed", "municipal_certificate_issued"],
        consumed_events=["citizen_updated", "identity_verified", "payment_confirmed"],
    ))


def _build_seguranca_social(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="mapTss", name="Ministério da Administração Pública e Segurança Social",
        org_type=OrganizationType.MINISTRY, module="seguranca-social", code="MAPTSS",
    ))
    orgs.register(Organization(
        id="inss", name="Instituto Nacional de Segurança Social",
        org_type=OrganizationType.PROVINCIAL_DIRECTORATE, module="seguranca-social",
        parent_id="mapTss",
    ))
    registry.register(ModuleRegistry(
        module="seguranca-social", name="Segurança Social",
        description="Contribuições, prestações sociais, registo empregador e benefícios",
        owner_ministry="Ministério da Administração Pública e Segurança Social",
        owner_ministry_code="MAPTSS",
        responsible_entity="Instituto Nacional de Segurança Social",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_MUNICIPAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["unidade", "municipio", "provincia"],
        enabled_services=["registo_empregador", "contribuicao", "prestacao_social", "pensao"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_MUNICIPIO", "ROLE_UNIDADE"],
        api_prefix="/api/v1/seguranca-social",
        exposed_events=["employer_registered", "social_contribution_received", "benefit_granted"],
        consumed_events=["citizen_updated", "identity_verified", "payment_confirmed", "company_incorporated"],
    ))


def _build_integracao_nacional(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    # Subdomínio BI
    orgs.register(Organization(
        id="dni", name="Direção Nacional de Identificação",
        org_type=OrganizationType.PROVINCIAL_DIRECTORATE, module="integracao-nacional", code="DNI",
    ))
    registry.register(ModuleRegistry(
        module="integracao-nacional-bi", name="Integração Nacional — BI",
        description="Verificação e consulta de Bilhete de Identidade via plataforma integrada",
        owner_ministry="Ministério do Interior", owner_ministry_code="MININT",
        responsible_entity="Direção Nacional de Identificação",
        territorial_model=TerritorialModel.NACIONAL_ONLY,
        status=ModuleStatus.ACTIVE,
        approval_chain=["nacional"],
        enabled_services=["verificar_bi", "consultar_bi"],
        required_roles=["ROLE_MINISTERIO", "ROLE_UNIDADE"],
        api_prefix="/api/v1/integracao-nacional/bi",
        exposed_events=["bi_verified", "bi_consulted"],
        consumed_events=["citizen_updated", "identity_verified"],
    ))
    # Subdomínio NIF
    registry.register(ModuleRegistry(
        module="integracao-nacional-nif", name="Integração Nacional — NIF",
        description="Verificação de Número de Identificação Fiscal",
        owner_ministry="Ministério das Finanças", owner_ministry_code="MINFIN",
        responsible_entity="Administração Geral Tributária",
        territorial_model=TerritorialModel.NACIONAL_ONLY,
        status=ModuleStatus.ACTIVE,
        approval_chain=["nacional"],
        enabled_services=["verificar_nif", "consultar_nif"],
        required_roles=["ROLE_MINISTERIO", "ROLE_UNIDADE"],
        api_prefix="/api/v1/integracao-nacional/nif",
        exposed_events=["nif_verified"],
        consumed_events=["citizen_updated", "nif_issued"],
    ))


def _build_apoio_empresarial(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="minecon", name="Ministério da Economia", org_type=OrganizationType.MINISTRY,
        module="apoio-empresarial", code="MINECON",
    ))
    registry.register(ModuleRegistry(
        module="apoio-empresarial", name="Apoio Empresarial",
        description="Abertura, licenciamento e suporte ao setor empresarial",
        owner_ministry="Ministério da Economia", owner_ministry_code="MINECON",
        responsible_entity="Direção Nacional de Apoio à Empresa",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["unidade", "provincia"],
        enabled_services=["registar_empresa", "licenciamento_comercial", "apoio_financeiro", "consultoria"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_UNIDADE"],
        api_prefix="/api/v1/apoio-empresarial",
        exposed_events=["company_registered", "commercial_license_issued", "business_support_granted"],
        consumed_events=["citizen_updated", "identity_verified", "payment_confirmed", "nif_issued"],
    ))


def _build_comercio(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="minecon", name="Ministério da Economia", org_type=OrganizationType.MINISTRY,
        module="comercio", code="MINECON",
    ))
    registry.register(ModuleRegistry(
        module="comercio", name="Comércio",
        description="Regulação comercial, alvarás e autorizações económicas",
        owner_ministry="Ministério da Economia", owner_ministry_code="MINECON",
        responsible_entity="Direção Nacional do Comércio",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_UNIDADE,
        status=ModuleStatus.DEVELOPMENT,
        approval_chain=["unidade", "provincia"],
        enabled_services=["registar_comercio", "emitir_alvara", "inspecao_comercial"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_UNIDADE"],
        api_prefix="/api/v1/comercio",
        exposed_events=["trade_registered", "license_permit_issued", "inspection_completed"],
        consumed_events=["citizen_updated", "identity_verified", "company_registered", "payment_confirmed"],
    ))


def _build_emprego(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="mapTss", name="Ministério da Administração Pública e Segurança Social",
        org_type=OrganizationType.MINISTRY, module="emprego", code="MAPTSS",
    ))
    registry.register(ModuleRegistry(
        module="emprego", name="Emprego",
        description="Intermediação laboral, vagas de emprego e colocação profissional",
        owner_ministry="Ministério da Administração Pública e Segurança Social",
        owner_ministry_code="MAPTSS",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_UNIDADE,
        status=ModuleStatus.ACTIVE,
        approval_chain=["unidade", "provincia"],
        enabled_services=["registar_contrato", "publicar_vaga", "intermediacao_colocacao"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_UNIDADE"],
        api_prefix="/api/v1/emprego",
        exposed_events=["employment_contract_registered", "job_vacancy_created", "placement_completed"],
        consumed_events=["citizen_updated", "identity_verified", "employer_registered"],
    ))


def _build_trabalho_inspecao(orgs: OrganizationTree, registry: RegistryCatalog) -> None:
    orgs.register(Organization(
        id="mapTss", name="Ministério da Administração Pública e Segurança Social",
        org_type=OrganizationType.MINISTRY, module="trabalho-inspecao", code="MAPTSS",
    ))
    registry.register(ModuleRegistry(
        module="trabalho-inspecao", name="Trabalho e Inspeção",
        description="Inspeção laboral, relações de trabalho e segurança ocupacional",
        owner_ministry="Ministério da Administração Pública e Segurança Social",
        owner_ministry_code="MAPTSS",
        territorial_model=TerritorialModel.NACIONAL_PROVINCIAL_UNIDADE,
        status=ModuleStatus.DEVELOPMENT,
        approval_chain=["unidade", "provincia"],
        enabled_services=["agendar_inspecao", "realizar_inspecao", "emitir_auto"],
        required_roles=["ROLE_MINISTERIO", "ROLE_PROVINCIA", "ROLE_UNIDADE"],
        api_prefix="/api/v1/trabalho-inspecao",
        exposed_events=["inspection_scheduled", "inspection_completed", "fine_issued"],
        consumed_events=["citizen_updated", "identity_verified", "employer_registered", "employment_contract_registered"],
    ))


def _register_tenants(manager: TenantManager) -> None:
    for module_id, name in [
        ("educacao", "Educação"),
        ("saude", "Saúde"),
        ("justica", "Justiça"),
        ("identity", "Identificação Civil"),
        ("payment", "Pagamentos"),
        ("registo-civil", "Registo Civil"),
        ("financas-impostos", "Finanças e Impostos"),
        ("administracao-local", "Administração Local"),
        ("seguranca-social", "Segurança Social"),
        ("integracao-nacional-bi", "Integração — BI"),
        ("integracao-nacional-nif", "Integração — NIF"),
        ("apoio-empresarial", "Apoio Empresarial"),
        ("comercio", "Comércio"),
        ("emprego", "Emprego"),
        ("trabalho-inspecao", "Trabalho e Inspeção"),
    ]:
        manager.register(Tenant(
            id=f"tenant-{module_id}",
            module=module_id,
            name=name,
            status=TenantStatus.ACTIVE,
            config={"api_version": "1.0.0", "log_level": "INFO"},
        ))


def bootstrap_governance() -> tuple[RegistryCatalog, OrganizationTree, TenantManager]:
    """Inicializa toda a camada de governança com os módulos core."""
    registry = RegistryCatalog()
    orgs = OrganizationTree()
    tenants = TenantManager()

    _build_educacao(orgs, registry)
    _build_saude(orgs, registry)
    _build_justica(orgs, registry)
    _build_identity(orgs, registry)
    _build_payment(orgs, registry)
    _build_registo_civil(orgs, registry)
    _build_financas_impostos(orgs, registry)
    _build_administracao_local(orgs, registry)
    _build_seguranca_social(orgs, registry)
    _build_integracao_nacional(orgs, registry)
    _build_apoio_empresarial(orgs, registry)
    _build_comercio(orgs, registry)
    _build_emprego(orgs, registry)
    _build_trabalho_inspecao(orgs, registry)
    _register_tenants(tenants)

    return registry, orgs, tenants


def bootstrap_summary() -> dict:
    """Relatório do bootstrap para diagnóstico."""
    registry, orgs, tenants = bootstrap_governance()
    return {
        "modules": {m.module: {
            "name": m.name,
            "ministry": m.owner_ministry_code,
            "status": m.status.value,
            "services": len(m.enabled_services),
            "territorial_model": m.territorial_model.value,
        } for m in registry.list_all()},
        "organizations": {
            "total": orgs.count(),
            "ministries": len(orgs.get_by_type(OrganizationType.MINISTRY)),
        },
        "tenants": {
            "total": len(tenants.list_all()),
            "active": len(tenants.list_active()),
        },
        "events": {
            "total_exposed": sum(len(m.exposed_events) for m in registry.list_all()),
            "total_consumed": sum(len(m.consumed_events) for m in registry.list_all()),
            "by_module": {m.module: {
                "exposes": m.exposed_events,
                "consumes": m.consumed_events,
            } for m in registry.list_all()},
        },
    }
