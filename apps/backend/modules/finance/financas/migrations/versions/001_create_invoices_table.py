"""Create invoices table

Revision ID: 001_create_invoices
Create Date: 2026-02-10

Nota: Este ficheiro é um stub documental. As migrações reais são geridas
pelo Alembic central em `alembic_core/`. Este ficheiro serve como contrato
de schema do módulo financeiro.
"""

# Schema de referência para a tabela invoices:
#
# CREATE TABLE invoices (
#     id VARCHAR PRIMARY KEY,
#     citizen_id VARCHAR NOT NULL,
#     reference VARCHAR NOT NULL UNIQUE,
#     revenue_code VARCHAR(32) NOT NULL,
#     cost_center VARCHAR(32) NOT NULL,
#     service_code VARCHAR(32) NOT NULL,
#     service_name VARCHAR(255) NOT NULL,
#     amount NUMERIC(15, 2) NOT NULL,
#     currency VARCHAR(3) DEFAULT 'AOA' NOT NULL,
#     status VARCHAR(20) DEFAULT 'PENDING' NOT NULL,
#     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
#     updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
#     due_date TIMESTAMP WITH TIME ZONE NOT NULL
# );
#
# CREATE INDEX ix_invoices_citizen_id ON invoices (citizen_id);
# CREATE INDEX ix_invoices_reference ON invoices (reference);
# CREATE INDEX ix_invoices_revenue_code ON invoices (revenue_code);
# CREATE INDEX ix_invoices_cost_center ON invoices (cost_center);
# CREATE INDEX ix_invoices_status ON invoices (status);