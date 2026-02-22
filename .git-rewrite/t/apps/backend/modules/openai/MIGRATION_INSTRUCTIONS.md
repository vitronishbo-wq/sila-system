Run Alembic migration to add the new `openai_chat_sessions` and `openai_chat_messages`
tables.

1. Ensure `alembic` is configured and `alembic.ini` points to your database.
2. From `apps/backend` (where your backend package root is):

```bash
source .venv/bin/activate
export PYTHONPATH=$(pwd)
alembic revision --autogenerate -m "add openai chat tables"
alembic upgrade head
```

If your project uses a different alembic setup, adapt commands accordingly. The models
are in `apps/backend/modules/openai/models.py`.
