from apps.backend.app.core.catalog.blueprint import (
    ESSENTIAL_MODULE_SLUGS,
    MODULE_BLUEPRINTS,
    build_service_blueprints,
)


def test_blueprint_has_institutional_scale():
    services = build_service_blueprints(900)
    assert len(MODULE_BLUEPRINTS) >= 50
    assert len(services) >= 900


def test_services_are_unique_and_linked_to_modules():
    services = build_service_blueprints(900)
    codes = [service.code for service in services]
    module_slugs = {module.slug for module in MODULE_BLUEPRINTS}
    assert len(codes) == len(set(codes))
    assert all(service.module_slug in module_slugs for service in services)


def test_essential_modules_are_present():
    module_slugs = {module.slug for module in MODULE_BLUEPRINTS}
    assert ESSENTIAL_MODULE_SLUGS.issubset(module_slugs)


def test_educacao_uses_citizen_goal_services():
    services = [
        service for service in build_service_blueprints(900) if service.module_slug == "educacao"
    ]
    service_names = {service.name for service in services}

    assert "Nova Matricula Escolar" in service_names
    assert "Transferencia Escolar" in service_names
    assert "Consultar Historico Escolar" in service_names
    assert "Reconhecimento de Diploma" in service_names

    forbidden_public_names = {
        "Agendamento de matricula escolar",
        "Atualizacao cadastral de matricula escolar",
        "Certificacao de matricula escolar",
        "Licenciamento de matricula escolar",
        "Pagamento de matricula escolar",
        "Revalidacao de matricula escolar",
    }
    assert service_names.isdisjoint(forbidden_public_names)
