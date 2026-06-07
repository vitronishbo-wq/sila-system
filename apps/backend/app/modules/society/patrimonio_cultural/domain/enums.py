from enum import StrEnum


class AssetType(StrEnum):
    MONUMENT = "monument"
    ARCHAEOLOGICAL_SITE = "archaeological_site"
    HISTORIC_BUILDING = "historic_building"
    CULTURAL_LANDSCAPE = "cultural_landscape"
    INTANGIBLE_HERITAGE = "intangible_heritage"
    MUSEUM_COLLECTION = "museum_collection"
    ARCHAEOLOGICAL_ARTIFACT = "archaeological_artifact"
    TRADITIONAL_KNOWLEDGE = "traditional_knowledge"


class AssetStatus(StrEnum):
    REGISTERED = "registered"
    UNDER_EVALUATION = "under_evaluation"
    PROTECTED = "protected"
    RESTORED = "restored"
    DEGRADED = "degraded"
    DESTROYED = "destroyed"


class ClassificationLevel(StrEnum):
    MUNICIPAL = "municipal"
    PROVINCIAL = "provincial"
    NATIONAL = "national"
    UNESCO = "unesco"
    WORLD_HERITAGE = "world_heritage"


class ClassificationType(StrEnum):
    HISTORIC = "historic"
    ARTISTIC = "artistic"
    ARCHAEOLOGICAL = "archaeological"
    ETHNOGRAPHIC = "ethnographic"
    PALEONTOLOGICAL = "paleontological"
    INDUSTRIAL = "industrial"
    RELIGIOUS = "religious"


class ActionType(StrEnum):
    CONSERVATION = "conservation"
    RESTORATION = "restoration"
    DOCUMENTATION = "documentation"
    RESEARCH = "research"
    MONITORING = "monitoring"
    EMERGENCY_INTERVENTION = "emergency_intervention"
