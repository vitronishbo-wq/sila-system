from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class SendNotificationCommand:
    notification_id: str
    recipient: str
    message: str
    notification_type: str

class SendNotificationCommandHandler(ABC):

    @abstractmethod
    async def execute(self, command: SendNotificationCommand) -> None:
        pass

@dataclass
class MarkNotificationAsReadCommand:
    notification_id: str

class MarkNotificationAsReadCommandHandler(ABC):

    @abstractmethod
    async def execute(self, command: MarkNotificationAsReadCommand) -> None:
        pass

@dataclass
class DeleteNotificationCommand:
    notification_id: str

class DeleteNotificationCommandHandler(ABC):

    @abstractmethod
    async def execute(self, command: DeleteNotificationCommand) -> None:
        pass