from app.core.events.event_versioning.version_registry import EventVersionRegistry

class EventUpcaster:

    @staticmethod
    def upcast(event):
        event_name = getattr(event, 'name', None)
        event_version = getattr(event, 'version', None)
        if event_name is None and isinstance(event, dict):
            event_name = event.get('name')
            event_version = event.get('version')
        transformer = EventVersionRegistry.get(event_name, event_version)
        if transformer:
            return transformer(event)
        return event