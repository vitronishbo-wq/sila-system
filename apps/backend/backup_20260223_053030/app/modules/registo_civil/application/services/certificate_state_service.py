class CivilStateCertificateService:
    async def issue(self, citizen_id: str):
        # Emissão de certificado de estado civil (Mock)
        return {
            "citizen_id": citizen_id,
            "civil_state": "single",
            "document_type": "CIVIL_STATE_CERTIFICATE",
            "issued_at": "2026-02-09T22:00:00Z"
        }
