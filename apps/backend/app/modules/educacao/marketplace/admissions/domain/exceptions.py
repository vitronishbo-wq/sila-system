"""Domain exceptions for Admissions subdomain"""


class AdmissionException(Exception):
    """Base exception for Admissions subdomain"""
    pass


class ApplicantNotEligible(AdmissionException):
    """Candidato não elegível para admissão"""
    pass


class RequiredDocumentsMissing(AdmissionException):
    """Documentos obrigatórios faltando"""
    pass


class AdmissionAlreadyProcessed(AdmissionException):
    """Admissão já foi processada"""
    pass


class AdmissionValidationFailed(AdmissionException):
    """Validação de admissão falhou"""
    pass


class DocumentVerificationFailed(AdmissionException):
    """Verificação de documentos falhou"""
    pass
