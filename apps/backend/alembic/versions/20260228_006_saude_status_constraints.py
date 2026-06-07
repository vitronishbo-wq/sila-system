"""backfill and add status check constraints for saude fases 4-7

Revision ID: 20260228_006_saude_status_ck
Revises: 20260228_005_saude_fases_4_7
Create Date: 2026-02-28 05:35:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260228_006_saude_status_ck"
down_revision = "20260228_005_saude_fases_4_7"
branch_labels = None
depends_on = None


STATUS_RULES: list[dict[str, object]] = [
    # Fase 4
    {
        "table": "health_vigilancia_epidemiologica",
        "default": "reported",
        "allowed": ["reported", "investigating", "contained", "closed"],
    },
    {
        "table": "health_notificacoes_surto",
        "default": "open",
        "allowed": ["open", "acknowledged", "closed"],
    },
    {
        "table": "health_controle_vetores",
        "default": "planned",
        "allowed": ["planned", "in_progress", "completed", "cancelled"],
    },
    {
        "table": "health_controle_zoonoses",
        "default": "planned",
        "allowed": ["planned", "in_progress", "completed", "cancelled"],
    },
    {
        "table": "health_monitorizacao_hidrica",
        "default": "monitoring",
        "allowed": ["monitoring", "alert", "mitigated", "closed"],
    },
    {
        "table": "health_alertas_saude",
        "default": "issued",
        "allowed": ["issued", "acknowledged", "resolved", "cancelled"],
    },
    # Fase 5
    {
        "table": "health_inspecoes_sanitarias",
        "default": "scheduled",
        "allowed": ["scheduled", "in_progress", "approved", "rejected", "cancelled"],
    },
    {
        "table": "health_licencas_sanitarias",
        "default": "requested",
        "allowed": ["requested", "under_review", "approved", "rejected", "suspended"],
    },
    {
        "table": "health_licencas_temporarias",
        "default": "requested",
        "allowed": ["requested", "active", "expired", "revoked"],
    },
    {
        "table": "health_fiscalizacoes_alimentos",
        "default": "open",
        "allowed": ["open", "in_progress", "completed", "cancelled"],
    },
    {
        "table": "health_controle_qualidade_alimentos",
        "default": "pending",
        "allowed": ["pending", "analyzing", "approved", "reproved"],
    },
    {
        "table": "health_fiscalizacoes_cadeia_frio",
        "default": "open",
        "allowed": ["open", "in_progress", "completed", "cancelled"],
    },
    {
        "table": "health_controles_abate_publico",
        "default": "open",
        "allowed": ["open", "in_progress", "completed", "cancelled"],
    },
    {
        "table": "health_inspecoes_transporte_alimentar",
        "default": "open",
        "allowed": ["open", "in_progress", "completed", "cancelled"],
    },
    {
        "table": "health_apreensoes_produto",
        "default": "registered",
        "allowed": ["registered", "destined", "released"],
    },
    # Fase 6
    {
        "table": "health_programas_malaria",
        "default": "planned",
        "allowed": ["planned", "active", "completed", "cancelled"],
    },
    {
        "table": "health_programas_hiv",
        "default": "planned",
        "allowed": ["planned", "active", "completed", "cancelled"],
    },
    {
        "table": "health_programas_preventivos",
        "default": "planned",
        "allowed": ["planned", "active", "completed", "cancelled"],
    },
    {
        "table": "health_rastreios_tuberculose",
        "default": "requested",
        "allowed": ["requested", "in_progress", "completed", "cancelled"],
    },
    {
        "table": "health_triagens_diabetes",
        "default": "requested",
        "allowed": ["requested", "in_progress", "completed", "cancelled"],
    },
    # Fase 7
    {
        "table": "health_relatorios_seguranca_alimentar",
        "default": "draft",
        "allowed": ["draft", "published", "archived"],
    },
    {
        "table": "health_avaliacoes_risco_sanitario",
        "default": "open",
        "allowed": ["open", "mitigated", "closed"],
    },
    {
        "table": "health_emergencias_sanitarias",
        "default": "reported",
        "allowed": ["reported", "in_response", "resolved", "cancelled"],
    },
    {
        "table": "health_educacao_sanitaria",
        "default": "planned",
        "allowed": ["planned", "in_progress", "completed", "cancelled"],
    },
]


def _quote_values(values: list[str]) -> str:
    return ", ".join(f"'{value}'" for value in values)


def upgrade():
    for rule in STATUS_RULES:
        table = str(rule["table"])
        default = str(rule["default"])
        allowed = [str(value) for value in rule["allowed"]]
        allowed_sql = _quote_values(allowed)
        constraint = f"ck_{table}_status"

        op.execute(
            f"""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                      AND table_name = '{table}'
                      AND column_name = 'status'
                ) THEN
                    -- Normalize to lowercase before validation/backfill.
                    UPDATE {table}
                    SET status = lower(status)
                    WHERE status IS NOT NULL;

                    -- Backfill invalid or null values to the configured default.
                    UPDATE {table}
                    SET status = '{default}'
                    WHERE status IS NULL
                       OR status NOT IN ({allowed_sql});

                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = '{constraint}'
                          AND conrelid = '{table}'::regclass
                    ) THEN
                        ALTER TABLE {table}
                        ADD CONSTRAINT {constraint}
                        CHECK (status IN ({allowed_sql}));
                    END IF;
                END IF;
            END $$;
            """
        )


def downgrade():
    for rule in STATUS_RULES:
        table = str(rule["table"])
        constraint = f"ck_{table}_status"
        op.execute(
            f"""
            DO $$
            BEGIN
                IF to_regclass('public.{table}') IS NOT NULL THEN
                    ALTER TABLE {table}
                    DROP CONSTRAINT IF EXISTS {constraint};
                END IF;
            END $$;
            """
        )
