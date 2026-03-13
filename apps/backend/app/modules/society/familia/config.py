from pydantic import BaseModel

class FamiliaModuleSettings(BaseModel):
    family_code_prefix: str = 'FAM'
    max_members_per_family: int = 32
    projections_enabled: bool = True
    outbox_topic: str = 'familia.domain'
settings = FamiliaModuleSettings()