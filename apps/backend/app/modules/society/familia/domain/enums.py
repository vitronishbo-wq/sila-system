from enum import StrEnum

class FamilyStatus(StrEnum):
    ACTIVE = 'ACTIVE'
    DISSOLVED = 'DISSOLVED'
    MIGRATED = 'MIGRATED'

class MemberRole(StrEnum):
    HEAD = 'HEAD'
    MEMBER = 'MEMBER'
    DEPENDENT = 'DEPENDENT'

class RelationshipType(StrEnum):
    PARENT = 'PARENT'
    CHILD = 'CHILD'
    SPOUSE = 'SPOUSE'
    SIBLING = 'SIBLING'
    GUARDIAN = 'GUARDIAN'
    DEPENDENT = 'DEPENDENT'

class RelationshipStatus(StrEnum):
    ACTIVE = 'ACTIVE'
    TERMINATED = 'TERMINATED'

class DependencyType(StrEnum):
    LEGAL = 'LEGAL'
    ECONOMIC = 'ECONOMIC'
    HEALTH = 'HEALTH'
    EDUCATION = 'EDUCATION'