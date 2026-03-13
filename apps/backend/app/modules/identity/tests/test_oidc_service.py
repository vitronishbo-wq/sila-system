import pytest
from apps.backend.app.modules.identity.oidc_provider.application.oidc_service import OIDCService
from apps.backend.app.modules.identity.verifiable_credentials.infrastructure.repositories.revocation_repository import RevocationRepository


def test_issue_token_success():
    repo = RevocationRepository()
    service = OIDCService(repo)
    token = service.issue_token(
        subject="citizen-001",
        credential_id="http://sila.gov.ao/credentials/bi-123",
        registry_index=10,
        credential_subject={"name": "Ana Silva", "email": "ana@example.com", "bi": "BI-0001"},
    )
    assert token["token_type"] == "Bearer"
    assert token["credential_id"] == "http://sila.gov.ao/credentials/bi-123"
    assert token["claims"]["sub"] == "citizen-001"
    assert token["claims"]["name"] == "Ana Silva"
    assert token["claims"]["email"] == "ana@example.com"
    assert token["claims"]["document_number"] == "BI-0001"


def test_issue_token_revoked():
    repo = RevocationRepository()
    repo.revoke(10)
    service = OIDCService(repo)
    with pytest.raises(ValueError):
        service.issue_token(
            subject="citizen-002",
            credential_id="http://sila.gov.ao/credentials/bi-456",
            registry_index=10,
        )
