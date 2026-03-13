from app.core.bridges.identity_bridge import CitizenFUC
from .citizen_event_model import CitizenEventModel, EventType
CitizenModel = CitizenFUC
__all__ = ['CitizenModel', 'CitizenFUC', 'CitizenEventModel', 'EventType']