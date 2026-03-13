from enum import Enum

class ProcurementMethod(str, Enum):
    OPEN_COMPETITION = 'open_competition'
    LIMITED = 'limited'
    DIRECT_AWARD = 'direct_award'