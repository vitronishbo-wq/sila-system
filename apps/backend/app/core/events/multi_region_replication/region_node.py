class RegionNode:
    def __init__(self, name, endpoint):
        self.name = name
        self.endpoint = endpoint

    async def replicate(self, event):
        event_name = getattr(event, "name", None)
        if event_name is None and isinstance(event, dict):
            event_name = event.get("name")
        print(f"Replicating event {event_name} to {self.name}")
