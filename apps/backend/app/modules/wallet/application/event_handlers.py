from abc import ABC, abstractmethod


class WalletEventHandler(ABC):
    @abstractmethod
    async def handle_wallet_created(self, wallet_id: str) -> None:
        pass

    @abstractmethod
    async def handle_deposit_received(self, wallet_id: str, amount: float) -> None:
        pass

    @abstractmethod
    async def handle_withdrawal_processed(self, wallet_id: str, amount: float) -> None:
        pass
