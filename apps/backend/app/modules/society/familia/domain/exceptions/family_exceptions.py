from uuid import UUID

class FamilyDomainError(Exception):
    pass

class CitizenAlreadyInActiveFamilyError(FamilyDomainError):

    def __init__(self, citizen_id: UUID, existing_family_id: UUID):
        super().__init__(f'Cidadao {citizen_id} ja pertence ao agregado ativo {existing_family_id}')

class HeadMustBeAdultError(FamilyDomainError):

    def __init__(self, citizen_id: UUID, age: int):
        super().__init__(f'Cidadao {citizen_id} com idade {age} nao pode ser chefe de agregado')

class BiologicalCoherenceError(FamilyDomainError):

    def __init__(self, parent_id: UUID, child_id: UUID, message: str):
        super().__init__(f'Relacao biologica invalida: {message}')
        self.parent_id = parent_id
        self.child_id = child_id

class ExclusiveMarriageError(FamilyDomainError):

    def __init__(self, citizen_id: UUID, active_spouse_id: UUID):
        super().__init__(f'Cidadao {citizen_id} ja possui relacao conjugal ativa com {active_spouse_id}')

class MinorRequiresGuardianError(FamilyDomainError):

    def __init__(self, minor_id: UUID):
        super().__init__(f'Menor {minor_id} requer tutor legal ativo')