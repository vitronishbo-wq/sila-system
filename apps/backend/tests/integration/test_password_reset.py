import os

import pytest

if settings.RUN_INTEGRATION != "1":
    pytest.skip(
        "Skipping password reset integration tests (set RUN_INTEGRATION=1 to enable)",
        allow_module_level=True,
    )


def test_placeholder():
    assert True
