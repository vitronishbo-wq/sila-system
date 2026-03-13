from apps.backend.app.modules.governance.statistics.application.bus import EventBus

def register_default_handlers(_: EventBus) -> None:
    """Hook for future event subscriptions."""