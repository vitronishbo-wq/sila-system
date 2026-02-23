import enum

class DocumentTypeEnum(str, enum.Enum):
    BI = "BI"
    PASSPORT = "PASSPORT"
    BIRTH_CERTIFICATE = "BIRTH_CERTIFICATE"
    DRIVER_LICENSE = "DRIVER_LICENSE"
    PHOTO = "PHOTO"
