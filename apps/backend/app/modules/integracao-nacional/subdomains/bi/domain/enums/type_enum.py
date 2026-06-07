from enum import StrEnum


class BiVerificationMethod(StrEnum):
    DIGITAL = "digital"
    PRESENCIAL = "presencial"
    BIOMETRICO = "biometrico"
    XROAD = "xroad"
    MANUAL = "manual"
