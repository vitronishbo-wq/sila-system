"""Catalog governance validation for institutional-scale service definitions."""

from app.core.catalog.blueprint import MODULE_BLUEPRINTS, build_service_blueprints


def test_catalog_scale_targets():
    services = build_service_blueprints(900)
    assert len(MODULE_BLUEPRINTS) >= 50
    assert len(services) >= 900


def test_catalog_service_codes_are_unique():
    services = build_service_blueprints(900)
    codes = [item.code for item in services]
    assert len(codes) == len(set(codes))


def test_catalog_service_metadata_mandatory_fields():
    services = build_service_blueprints(900)
    allowed_visibility = {"PUBLIC", "INTERNAL"}
    for item in services:
        assert item.workflow_template
        assert item.sla_days >= 1
        assert item.fee >= 0
        assert item.visibility in allowed_visibility
        assert item.required_documents


def test_catalog_has_no_orphan_services():
    services = build_service_blueprints(900)
    module_slugs = {module.slug for module in MODULE_BLUEPRINTS}
    assert all(item.module_slug in module_slugs for item in services)
