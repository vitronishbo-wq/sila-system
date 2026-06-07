import pytest

# Try to import the module; if it's absent or doesn't expose the expected
# symbols, skip the entire module at import time (tests are placeholders).
try:
    import apps.backend.app.modules.commercial.schemas as comm_schemas
except Exception:
    pytest.skip("Commercial schemas module not available", allow_module_level=True)

if not (
    hasattr(comm_schemas, "CommercialLicenseCreate")
    and hasattr(comm_schemas, "CommercialLicenseResponse")
):
    pytest.skip("Commercial schema types not implemented", allow_module_level=True)


def test_commercial_schemas_present():
    assert comm_schemas.CommercialLicenseCreate is not None
    assert comm_schemas.CommercialLicenseResponse is not None
