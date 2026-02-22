"""Add triggers and stored procedures

Revision ID: 006_add_triggers
Revises: 005_add_constraints
Create Date: 2024-01-06 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '006_add_triggers'
down_revision = '005_add_constraints'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create function to update updated_at timestamp
    op.execute("""
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = NOW();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # Create trigger for taxpayer table
    op.execute("""
    CREATE TRIGGER trigger_taxpayer_updated_at
    BEFORE UPDATE ON payment_taxpayers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
    """)
    
    # Create trigger for declaration table
    op.execute("""
    CREATE TRIGGER trigger_declaration_updated_at
    BEFORE UPDATE ON payment_declarations
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
    """)
    
    # Create trigger for debt table
    op.execute("""
    CREATE TRIGGER trigger_debt_updated_at
    BEFORE UPDATE ON payment_debts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
    """)
    
    # Create trigger for payment table
    op.execute("""
    CREATE TRIGGER trigger_payment_updated_at
    BEFORE UPDATE ON payment_payments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
    """)
    
    # Create trigger for certificate table
    op.execute("""
    CREATE TRIGGER trigger_certificate_updated_at
    BEFORE UPDATE ON payment_certificates
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
    """)
    
    # Create trigger for sequence table
    op.execute("""
    CREATE TRIGGER trigger_sequence_updated_at
    BEFORE UPDATE ON payment_sequences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
    """)
    
    # Create function to get next sequence value
    op.execute("""
    CREATE OR REPLACE FUNCTION get_next_sequence(p_type VARCHAR, p_year INTEGER)
    RETURNS INTEGER AS $$
    DECLARE
        v_next_value INTEGER;
    BEGIN
        UPDATE payment_sequences 
        SET last_value = last_value + 1
        WHERE sequence_type = p_type AND year = p_year
        RETURNING last_value INTO v_next_value;
        
        IF v_next_value IS NULL THEN
            INSERT INTO payment_sequences (id, sequence_type, year, last_value)
            VALUES (gen_random_uuid(), p_type, p_year, 1)
            RETURNING last_value INTO v_next_value;
        END IF;
        
        RETURN v_next_value;
    END;
    $$ LANGUAGE plpgsql;
    """)
    
    # Create function for soft deletes
    op.execute("""
    CREATE OR REPLACE FUNCTION soft_delete_entity(p_table VARCHAR, p_id UUID)
    RETURNS VOID AS $$
    BEGIN
        IF p_table = 'taxpayer' THEN
            UPDATE payment_taxpayers SET status = 'DELETED', updated_at = NOW() WHERE id = p_id;
        ELSIF p_table = 'declaration' THEN
            UPDATE payment_declarations SET status = 'CANCELLED', updated_at = NOW() WHERE id = p_id;
        ELSIF p_table = 'debt' THEN
            UPDATE payment_debts SET status = 'CANCELLED', updated_at = NOW() WHERE id = p_id;
        ELSIF p_table = 'payment' THEN
            UPDATE payment_payments SET status = 'CANCELLED', updated_at = NOW() WHERE id = p_id;
        ELSIF p_table = 'certificate' THEN
            UPDATE payment_certificates SET status = 'REVOKED', updated_at = NOW() WHERE id = p_id;
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)


def downgrade() -> None:
    op.execute("DROP FUNCTION IF EXISTS soft_delete_entity(VARCHAR, UUID)")
    op.execute("DROP FUNCTION IF EXISTS get_next_sequence(VARCHAR, INTEGER)")
    
    op.execute("DROP TRIGGER IF EXISTS trigger_sequence_updated_at ON payment_sequences")
    op.execute("DROP TRIGGER IF EXISTS trigger_certificate_updated_at ON payment_certificates")
    op.execute("DROP TRIGGER IF EXISTS trigger_payment_updated_at ON payment_payments")
    op.execute("DROP TRIGGER IF EXISTS trigger_debt_updated_at ON payment_debts")
    op.execute("DROP TRIGGER IF EXISTS trigger_declaration_updated_at ON payment_declarations")
    op.execute("DROP TRIGGER IF EXISTS trigger_taxpayer_updated_at ON payment_taxpayers")
    
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")
