Alembic migrations for foundation_outbox
=====================================

This repo includes a Postgres-ready Alembic revision that creates the
`foundation_outbox` table used by the SQL-backed Outbox implementation.

How to run (example using env DATABASE_URL):

```bash
export DATABASE_URL=postgresql+asyncpg://sila_user:Trumanmarcelo_1983@127.0.0.1:5432/sila_db
alembic -x async=true upgrade head
```

Notes:
- The migration uses `JSONB` for the `payload` column and `timestamp with time zone` for time fields.
- Ensure `alembic.ini` has `sqlalchemy.url = %(DATABASE_URL)s` or pass via env.
- For async engines (asyncpg) you may need to use Alembic's async configuration or run with `-x async=true` if your env supports it.
