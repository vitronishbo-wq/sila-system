from abc import ABC, abstractmethod


class NotificationEventHandler(ABC):
    @abstractmethod
    async def handle_notification_sent(self, notification_id: str) -> None:
        pass

    @abstractmethod
    async def handle_notification_read(self, notification_id: str) -> None:
        pass

    @abstractmethod
    async def handle_notification_deleted(self, notification_id: str) -> None:
        pass
