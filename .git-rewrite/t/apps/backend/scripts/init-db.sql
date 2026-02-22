-- ===========================================
-- SILA System - Inicialização do Banco de Dados
-- Executado automaticamente quando o container PostgreSQL inicia
-- ===========================================

-- Habilitar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Criar schema se não existir
CREATE SCHEMA IF NOT EXISTS sila_system;
SET search_path TO sila_system, public;

-- Criar tabela de usuários básica
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);

-- Criar tabela de auditoria
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(255),
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices para auditoria
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Inserir usuário admin padrão (senha: admin123)
INSERT INTO users (email, username, password_hash, full_name, is_superuser)
VALUES (
    'admin@sila.system',
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq9w5GS', -- admin123
    'SILA System Administrator',
    true
) ON CONFLICT (email) DO NOTHING;

-- Criar função para atualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Criar trigger para atualizar timestamp
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Criar view de estatísticas
CREATE OR REPLACE VIEW system_stats AS
SELECT
    'users' as table_name,
    COUNT(*) as total_records,
    COUNT(CASE WHEN is_active = true THEN 1 END) as active_records,
    MAX(created_at) as last_created
FROM users;

-- Grant permissions
GRANT USAGE ON SCHEMA sila_system TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA sila_system TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA sila_system TO postgres;

-- Log de inicialização
DO $$
BEGIN
    RAISE NOTICE '🚀 SILA System Database initialized successfully';
    RAISE NOTICE '📊 Tables created: users, audit_logs';
    RAISE NOTICE '👤 Default admin user: admin@sila.system / admin123';
END $$;
