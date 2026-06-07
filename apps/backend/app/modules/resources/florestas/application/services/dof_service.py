class DofService:
    async def health(self) -> dict[str, str]:
        return {"status": "ok"}
