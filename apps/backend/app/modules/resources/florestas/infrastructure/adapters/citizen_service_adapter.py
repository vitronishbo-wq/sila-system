class CitizenServiceAdapter:
    def __init__(self, dependency: object | None = None):
        self.dependency = dependency

    async def available(self) -> bool:
        return True
