"""Create payments table

Revision ID: 002_create_payments
Create Date: 2026-02-10

Nota: Stub documental. Migrações reais em `alembic_core/`.
"""

# Schema de referência para a tabela payments:
#
# CREATE TABLE payments (
#     id VARCHAR PRIMARY KEY,
#     invoice_id VARCHAR NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
#     citizen_id VARCHAR NOT NULL,
#     amount NUMERIC(15, 2) NOT NULL,
#     currency VARCHAR(3) DEFAULT 'AOA' NOT NULL,
#     gateway_reference VARCHAR NOT NULL UNIQUE,
#     status VARCHAR(20) DEFAULT 'PENDING' NOT NULL,
#     payment_method VARCHAR NOT NULL,
#     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
#     confirmed_at TIMESTAMP WITH TIME ZONE
# );
#
# CREATE INDEX ix_payments_invoice_id ON payments (invoice_id);
# CREATE INDEX ix_payments_citizen_id ON payments (citizen_id);
# CREATE INDEX ix_payments_gateway_reference ON payments (gateway_reference);
