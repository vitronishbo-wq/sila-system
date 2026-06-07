from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from typing import Any
from uuid import uuid4


class MessagePublisherPort(ABC):
    @abstractmethod
    async def publish(
        self,
        *,
        topic: str,
        payload: dict[str, Any],
        headers: dict[str, Any] | None = None,
        key: str | None = None,
    ) -> str:
        pass


class RabbitMQPublisher(MessagePublisherPort):
    def __init__(self, *, url: str, exchange: str = "sila.events") -> None:
        self._url = url
        self._exchange_name = exchange
        self._connection = None
        self._channel = None
        self._exchange = None

    async def _connect(self) -> None:
        if self._connection is not None:
            return
        try:
            import aio_pika
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Dependencia ausente: instale aio-pika para RabbitMQ publisher"
            ) from exc
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            self._exchange_name, type=aio_pika.ExchangeType.TOPIC, durable=True
        )

    async def publish(
        self,
        *,
        topic: str,
        payload: dict[str, Any],
        headers: dict[str, Any] | None = None,
        key: str | None = None,
    ) -> str:
        await self._connect()
        import aio_pika

        message_id = key or str(uuid4())
        body = json.dumps(payload, default=str).encode("utf-8")
        message = aio_pika.Message(
            body=body,
            content_type="application/json",
            headers=headers or {},
            message_id=message_id,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )
        await self._exchange.publish(message, routing_key=topic)
        return message_id


class KafkaPublisher(MessagePublisherPort):
    def __init__(self, *, bootstrap_servers: str) -> None:
        self._bootstrap_servers = bootstrap_servers
        self._producer = None

    async def _connect(self) -> None:
        if self._producer is not None:
            return
        try:
            from aiokafka import AIOKafkaProducer
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Dependencia ausente: instale aiokafka para Kafka publisher"
            ) from exc
        self._producer = AIOKafkaProducer(bootstrap_servers=self._bootstrap_servers)
        await self._producer.start()

    async def publish(
        self,
        *,
        topic: str,
        payload: dict[str, Any],
        headers: dict[str, Any] | None = None,
        key: str | None = None,
    ) -> str:
        await self._connect()
        body = json.dumps(payload, default=str).encode("utf-8")
        kafka_headers = []
        for header_key, header_value in (headers or {}).items():
            kafka_headers.append((str(header_key), str(header_value).encode("utf-8")))
        metadata = await self._producer.send_and_wait(
            topic, value=body, key=key.encode("utf-8") if key else None, headers=kafka_headers
        )
        return f"{metadata.topic}:{metadata.partition}:{metadata.offset}"


class NATSPublisher(MessagePublisherPort):
    def __init__(self, *, servers: list[str]) -> None:
        self._servers = servers
        self._client = None

    async def _connect(self) -> None:
        if self._client is not None:
            return
        try:
            import nats
        except ModuleNotFoundError as exc:
            raise RuntimeError("Dependencia ausente: instale nats-py para NATS publisher") from exc
        self._client = await nats.connect(servers=self._servers)

    async def publish(
        self,
        *,
        topic: str,
        payload: dict[str, Any],
        headers: dict[str, Any] | None = None,
        key: str | None = None,
    ) -> str:
        await self._connect()
        message_id = key or str(uuid4())
        envelope = {"message_id": message_id, "headers": headers or {}, "payload": payload}
        await self._client.publish(topic, json.dumps(envelope, default=str).encode("utf-8"))
        await self._client.flush()
        return message_id


class BrokerPublisherFactory:
    @staticmethod
    def from_env() -> MessagePublisherPort:
        driver = os.getenv("AGUAS_EVENT_BROKER", "rabbitmq").strip().lower()
        if driver == "rabbitmq":
            return RabbitMQPublisher(
                url=os.getenv("AGUAS_RABBITMQ_URL", "amqp://guest:guest@127.0.0.1:5672/"),
                exchange=os.getenv("AGUAS_RABBITMQ_EXCHANGE", "sila.events"),
            )
        if driver == "kafka":
            return KafkaPublisher(
                bootstrap_servers=os.getenv("AGUAS_KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")
            )
        if driver == "nats":
            raw_servers = os.getenv("AGUAS_NATS_SERVERS", "nats://127.0.0.1:4222")
            servers = [item.strip() for item in raw_servers.split(",") if item.strip()]
            return NATSPublisher(servers=servers)
        raise ValueError(f"Broker nao suportado para AGUAS_EVENT_BROKER: {driver}")
