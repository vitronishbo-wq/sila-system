Outbox Dispatcher
=================

Usage
-----

Run a one-shot dispatcher that reads `data/foundation_outbox.jsonl` and publishes events:

```bash
python -m apps.backend.app.modules.educacao.foundation.eventbus.dispatcher --bus local
```

Supported `--bus` values:
- `local` (default): logs events to stdout (safe for smoke tests)
- `rabbit`: publish to RabbitMQ (requires `pika` and `RABBITMQ_URL`)
- `kafka`: publish to Kafka (requires `confluent_kafka`)

Environment variables:
- `OUTBOX_PATH` - path to outbox file (default `data/foundation_outbox.jsonl`)
- `OUTBOX_BUS` - default bus when not passed via CLI
- `RABBITMQ_URL` - amqp url for RabbitMQ adapter
- `KAFKA_BOOTSTRAP` - bootstrap servers for Kafka adapter

Notes
-----
- The dispatcher rewrites the outbox file keeping failed records for retry.
- For production use a DB-backed outbox and a background worker (Celery/Temporal) for durability.

SQL-backed dispatcher
---------------------

This package includes a SQL-backed outbox and dispatcher for transactional claiming/flush.

Environment variables:
- `DATABASE_URL` - SQLAlchemy URL (defaults to `sqlite:///data/foundation_outbox.db`)
- `OUTBOX_BUS` - default bus (`local|rabbit|kafka`)

Run the SQL dispatcher once:

```bash
python -m apps.backend.app.modules.educacao.foundation.eventbus.dispatcher_sql --bus local
```

