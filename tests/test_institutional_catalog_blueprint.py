from app.core.catalog.blueprint import (
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
