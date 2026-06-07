from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CreateWalletCommand:
    wallet_id: str
    owner_id: str
    initial_balance: float


class CreateWalletCommandHandler(ABC):
    @abstractmethod
    async def execute(self, command: CreateWalletCommand) -> None:
        pass


@dataclass
class DepositCommand:
    wallet_id: str
    amount: float


class DepositCommandHandler(ABC):
    @abstractmethod
    async def execute(self, command: DepositCommand) -> None:
        pass


@dataclass
class WithdrawCommand:
    wallet_id: str
    amount: float


class WithdrawCommandHandler(ABC):
    @abstractmethod
    async def execute(self, command: WithdrawCommand) -> None:
        pass
