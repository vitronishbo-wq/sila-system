"""add saude tables for fases 4 to 7

Revision ID: 20260228_005_saude_fases_4_7
Revises: 20260228_004_educacao_foundation
Create Date: 2026-02-28 05:15:00.000000
"""

from alembic import op

revision = "20260228_005_saude_fases_4_7"
down_revision = "20260228_004_educacao_foundation"
branch_labels = None
depends_on = None


def upgrade():
    # Fase 4 - Vigilancia
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_vigilancia_epidemiologica (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            reported_by UUID NOT NULL,
            disease_name VARCHAR(120) NOT NULL,
            municipality VARCHAR(120) NOT NULL,
            suspected_cases INTEGER NOT NULL DEFAULT 0,
            confirmed_cases INTEGER NOT NULL DEFAULT 0,
            status VARCHAR(30) NOT NULL DEFAULT 'reported',
            notes VARCHAR(2000),
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            investigating_at TIMESTAMPTZ,
            contained_at TIMESTAMPTZ,
            closed_at TIMESTAMPTZ,
            closure_summary VARCHAR(2000)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_notificacoes_surto (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            vigilancia_id UUID,
            title VARCHAR(255) NOT NULL,
            description VARCHAR(2000) NOT NULL,
            severity VARCHAR(20) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'open',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            acknowledged_at TIMESTAMPTZ,
            closed_at TIMESTAMPTZ,
            closure_notes VARCHAR(2000)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_controle_vetores (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            vector_type VARCHAR(120) NOT NULL,
            area VARCHAR(120) NOT NULL,
            action_type VARCHAR(120) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'planned',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            report VARCHAR(2000),
            cancelled_at TIMESTAMPTZ,
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_controle_zoonoses (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            zoonotic_disease VARCHAR(120) NOT NULL,
            animal_type VARCHAR(120) NOT NULL,
            area VARCHAR(120) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'planned',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            report VARCHAR(2000),
            cancelled_at TIMESTAMPTZ,
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_monitorizacao_hidrica (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            area VARCHAR(120) NOT NULL,
            water_source VARCHAR(120) NOT NULL,
            contamination_index DOUBLE PRECISION NOT NULL DEFAULT 0,
            pathogen_detected VARCHAR(120),
            status VARCHAR(30) NOT NULL DEFAULT 'monitoring',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            alerted_at TIMESTAMPTZ,
            mitigated_at TIMESTAMPTZ,
            closed_at TIMESTAMPTZ,
            notes VARCHAR(2000)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_alertas_saude (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            title VARCHAR(255) NOT NULL,
            message VARCHAR(2000) NOT NULL,
            channel VARCHAR(20) NOT NULL,
            priority VARCHAR(20) NOT NULL DEFAULT 'medium',
            status VARCHAR(30) NOT NULL DEFAULT 'issued',
            issued_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            acknowledged_at TIMESTAMPTZ,
            resolved_at TIMESTAMPTZ,
            cancelled_at TIMESTAMPTZ,
            cancellation_reason VARCHAR(300)
        )
        """
    )

    # Fase 5 - Inspecao e Licenciamento
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_inspecoes_sanitarias (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            estabelecimento_nome VARCHAR(255) NOT NULL,
            estabelecimento_tipo VARCHAR(120) NOT NULL,
            localizacao VARCHAR(255) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'scheduled',
            scheduled_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            concluded_at TIMESTAMPTZ,
            report VARCHAR(2000),
            rejection_reason VARCHAR(300),
            cancelled_at TIMESTAMPTZ,
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_licencas_sanitarias (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            estabelecimento_nome VARCHAR(255) NOT NULL,
            numero_licenca VARCHAR(80) NOT NULL UNIQUE,
            atividade VARCHAR(120) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'requested',
            requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            reviewed_at TIMESTAMPTZ,
            approved_at TIMESTAMPTZ,
            rejected_at TIMESTAMPTZ,
            valid_until DATE,
            rejection_reason VARCHAR(300),
            suspended_at TIMESTAMPTZ,
            suspension_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_licencas_temporarias (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            estabelecimento_nome VARCHAR(255) NOT NULL,
            numero_permissao VARCHAR(80) NOT NULL UNIQUE,
            finalidade VARCHAR(255) NOT NULL,
            valid_from DATE NOT NULL,
            valid_to DATE NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'requested',
            requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            activated_at TIMESTAMPTZ,
            revoked_at TIMESTAMPTZ,
            revocation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_fiscalizacoes_alimentos (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            estabelecimento_nome VARCHAR(255) NOT NULL,
            categoria_produto VARCHAR(120) NOT NULL,
            achados_iniciais VARCHAR(2000) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'open',
            opened_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            report VARCHAR(2000),
            cancelled_at TIMESTAMPTZ,
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_controle_qualidade_alimentos (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            produto_nome VARCHAR(255) NOT NULL,
            lote VARCHAR(80) NOT NULL,
            indice_qualidade DOUBLE PRECISION NOT NULL DEFAULT 0,
            status VARCHAR(30) NOT NULL DEFAULT 'pending',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            analyzed_at TIMESTAMPTZ,
            decided_at TIMESTAMPTZ,
            notes VARCHAR(2000)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_fiscalizacoes_cadeia_frio (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            unidade_nome VARCHAR(255) NOT NULL,
            temperatura_min DOUBLE PRECISION NOT NULL,
            temperatura_max DOUBLE PRECISION NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'open',
            opened_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            report VARCHAR(2000),
            cancelled_at TIMESTAMPTZ,
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_controles_abate_publico (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            matadouro_nome VARCHAR(255) NOT NULL,
            quantidade_animais INTEGER NOT NULL DEFAULT 0,
            condicoes_sanitarias VARCHAR(2000) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'open',
            opened_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            report VARCHAR(2000),
            cancelled_at TIMESTAMPTZ,
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_inspecoes_transporte_alimentar (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            transportadora_nome VARCHAR(255) NOT NULL,
            placa_veiculo VARCHAR(50) NOT NULL,
            tipo_carga VARCHAR(120) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'open',
            opened_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            report VARCHAR(2000),
            cancelled_at TIMESTAMPTZ,
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_apreensoes_produto (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            produto_nome VARCHAR(255) NOT NULL,
            quantidade INTEGER NOT NULL,
            motivo VARCHAR(1000) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'registered',
            registered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            destined_at TIMESTAMPTZ,
            released_at TIMESTAMPTZ,
            destination_notes VARCHAR(1000),
            release_reason VARCHAR(300)
        )
        """
    )

    # Fase 6 - Programas e Rastreios
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_programas_malaria (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            campaign_name VARCHAR(255) NOT NULL,
            region VARCHAR(120) NOT NULL,
            target_population INTEGER NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'planned',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            cancelled_at TIMESTAMPTZ,
            summary VARCHAR(2000),
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_programas_hiv (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            program_name VARCHAR(255) NOT NULL,
            municipality VARCHAR(120) NOT NULL,
            monthly_test_goal INTEGER NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'planned',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            cancelled_at TIMESTAMPTZ,
            summary VARCHAR(2000),
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_programas_preventivos (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            title VARCHAR(255) NOT NULL,
            audience VARCHAR(120) NOT NULL,
            channel VARCHAR(20) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'planned',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            cancelled_at TIMESTAMPTZ,
            summary VARCHAR(2000),
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_rastreios_tuberculose (
            id UUID PRIMARY KEY,
            citizen_id UUID NOT NULL,
            created_by UUID NOT NULL,
            health_unit_id UUID NOT NULL,
            sintomas VARCHAR(1000) NOT NULL,
            risk_score INTEGER NOT NULL DEFAULT 0,
            status VARCHAR(30) NOT NULL DEFAULT 'requested',
            requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            screened_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            result_summary VARCHAR(2000),
            cancelled_at TIMESTAMPTZ,
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_triagens_diabetes (
            id UUID PRIMARY KEY,
            citizen_id UUID NOT NULL,
            created_by UUID NOT NULL,
            health_unit_id UUID NOT NULL,
            fasting_glucose DOUBLE PRECISION NOT NULL DEFAULT 0,
            risk_factors VARCHAR(1000) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'requested',
            requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            screened_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            result_summary VARCHAR(2000),
            cancelled_at TIMESTAMPTZ,
            cancellation_reason VARCHAR(300)
        )
        """
    )

    # Fase 7 - Relatorios e Avaliacoes
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_relatorios_seguranca_alimentar (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            titulo VARCHAR(255) NOT NULL,
            area VARCHAR(120) NOT NULL,
            findings VARCHAR(3000) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'draft',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            published_at TIMESTAMPTZ,
            archived_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_avaliacoes_risco_sanitario (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            entidade_nome VARCHAR(255) NOT NULL,
            risco_score DOUBLE PRECISION NOT NULL DEFAULT 0,
            observacoes VARCHAR(3000) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'open',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            mitigated_at TIMESTAMPTZ,
            closed_at TIMESTAMPTZ,
            mitigation_notes VARCHAR(2000),
            closure_notes VARCHAR(2000)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_emergencias_sanitarias (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            incidente VARCHAR(255) NOT NULL,
            localizacao VARCHAR(255) NOT NULL,
            severidade VARCHAR(80) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'reported',
            reported_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            response_started_at TIMESTAMPTZ,
            resolved_at TIMESTAMPTZ,
            cancelled_at TIMESTAMPTZ,
            response_notes VARCHAR(2000),
            resolution_notes VARCHAR(2000),
            cancellation_reason VARCHAR(300)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS health_educacao_sanitaria (
            id UUID PRIMARY KEY,
            health_unit_id UUID NOT NULL,
            created_by UUID NOT NULL,
            tema VARCHAR(255) NOT NULL,
            publico_alvo VARCHAR(120) NOT NULL,
            formato VARCHAR(120) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'planned',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            started_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ,
            cancelled_at TIMESTAMPTZ,
            summary VARCHAR(2000),
            cancellation_reason VARCHAR(300)
        )
        """
    )

    # Indices
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hvig_epi_health_unit ON health_vigilancia_epidemiologica (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hvig_notif_health_unit ON health_notificacoes_surto (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hvig_notif_vigilancia ON health_notificacoes_surto (vigilancia_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hvig_vetor_health_unit ON health_controle_vetores (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hvig_zoonose_health_unit ON health_controle_zoonoses (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hvig_hidrica_health_unit ON health_monitorizacao_hidrica (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hvig_alerta_health_unit ON health_alertas_saude (health_unit_id)"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hinsp_san_health_unit ON health_inspecoes_sanitarias (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hlic_san_health_unit ON health_licencas_sanitarias (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hlic_tmp_health_unit ON health_licencas_temporarias (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hfisc_alim_health_unit ON health_fiscalizacoes_alimentos (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hqual_alim_health_unit ON health_controle_qualidade_alimentos (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hcadeia_frio_health_unit ON health_fiscalizacoes_cadeia_frio (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_habate_health_unit ON health_controles_abate_publico (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_htransp_alim_health_unit ON health_inspecoes_transporte_alimentar (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hapre_prod_health_unit ON health_apreensoes_produto (health_unit_id)"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hprog_mal_health_unit ON health_programas_malaria (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hprog_hiv_health_unit ON health_programas_hiv (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hprog_prev_health_unit ON health_programas_preventivos (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hrast_tb_citizen ON health_rastreios_tuberculose (citizen_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hrast_tb_health_unit ON health_rastreios_tuberculose (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_htriag_diab_citizen ON health_triagens_diabetes (citizen_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_htriag_diab_health_unit ON health_triagens_diabetes (health_unit_id)"
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hrel_seg_alim_health_unit ON health_relatorios_seguranca_alimentar (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_haval_risco_health_unit ON health_avaliacoes_risco_sanitario (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_hemerg_san_health_unit ON health_emergencias_sanitarias (health_unit_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_heduc_san_health_unit ON health_educacao_sanitaria (health_unit_id)"
    )


def downgrade():
    op.execute("DROP TABLE IF EXISTS health_educacao_sanitaria")
    op.execute("DROP TABLE IF EXISTS health_emergencias_sanitarias")
    op.execute("DROP TABLE IF EXISTS health_avaliacoes_risco_sanitario")
    op.execute("DROP TABLE IF EXISTS health_relatorios_seguranca_alimentar")

    op.execute("DROP TABLE IF EXISTS health_triagens_diabetes")
    op.execute("DROP TABLE IF EXISTS health_rastreios_tuberculose")
    op.execute("DROP TABLE IF EXISTS health_programas_preventivos")
    op.execute("DROP TABLE IF EXISTS health_programas_hiv")
    op.execute("DROP TABLE IF EXISTS health_programas_malaria")

    op.execute("DROP TABLE IF EXISTS health_apreensoes_produto")
    op.execute("DROP TABLE IF EXISTS health_inspecoes_transporte_alimentar")
    op.execute("DROP TABLE IF EXISTS health_controles_abate_publico")
    op.execute("DROP TABLE IF EXISTS health_fiscalizacoes_cadeia_frio")
    op.execute("DROP TABLE IF EXISTS health_controle_qualidade_alimentos")
    op.execute("DROP TABLE IF EXISTS health_fiscalizacoes_alimentos")
    op.execute("DROP TABLE IF EXISTS health_licencas_temporarias")
    op.execute("DROP TABLE IF EXISTS health_licencas_sanitarias")
    op.execute("DROP TABLE IF EXISTS health_inspecoes_sanitarias")

    op.execute("DROP TABLE IF EXISTS health_alertas_saude")
    op.execute("DROP TABLE IF EXISTS health_monitorizacao_hidrica")
    op.execute("DROP TABLE IF EXISTS health_controle_zoonoses")
    op.execute("DROP TABLE IF EXISTS health_controle_vetores")
    op.execute("DROP TABLE IF EXISTS health_notificacoes_surto")
    op.execute("DROP TABLE IF EXISTS health_vigilancia_epidemiologica")
