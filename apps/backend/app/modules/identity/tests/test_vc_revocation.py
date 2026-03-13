import pytest
from apps.backend.app.modules.identity.verifiable_credentials.infrastructure.repositories.revocation_repository import RevocationRepository
from apps.backend.app.modules.identity.verifiable_credentials.application.services.revocation_service import RevocationService

def test_credential_revocation_logic():
    repo = RevocationRepository()
    service = RevocationService(repo)

    cred_id = "http://sila.gov.ao/credentials/bi-789"
    index = 100

    # Pre-condicao: Valida
    assert repo.is_revoked(index) is False

    # Execucao: Revogar
    result = service.invalidate_credential(cred_id, index)

    # Pos-condicao: Revogada
    assert result["status"] == "revoked"
    assert repo.is_revoked(index) is True

    # Verificacao de compressao
    status_list = repo.get_compressed_status_list()
    assert len(status_list) > 0
    print(f"\n✅ Revogacao Processada: {cred_id} -> Index {index}")
    print(f"📦 StatusList (B64): {status_list[:25]}...")
