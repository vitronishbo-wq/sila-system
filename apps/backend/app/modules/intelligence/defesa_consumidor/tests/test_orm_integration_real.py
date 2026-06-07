import os

import pytest


@pytest.mark.integration
def test_guardrail_db_url_configurada_para_integracao():
    url = os.environ.get("DATABASE_URL")
    if not url:
        pytest.skip("DATABASE_URL nao configurada para integracao real")
    assert "postgresql" in url
