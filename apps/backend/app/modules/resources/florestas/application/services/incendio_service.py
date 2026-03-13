class IncendioService:

    async def health(self) -> dict[str, str]:
        return {'status': 'ok'}