from apps.backend.app.modules.identity.subdomains.verifiable_credentials.infrastructure.repositories.revocation_repository import RevocationRepository

class RevocationService:

    def __init__(self, repository: RevocationRepository):
        self.repository = repository

    def invalidate_credential(self, credential_id: str, registry_index: int) -> dict:
        """Marca uma credencial como invalida no registro soberano."""
        self.repository.revoke(registry_index)
        return {'credential_id': credential_id, 'status': 'revoked', 'registry_index': registry_index}