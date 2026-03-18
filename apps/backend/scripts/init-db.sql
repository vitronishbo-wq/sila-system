CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

CREATE SCHEMA IF NOT EXISTS sila_system;
SET search_path TO sila_system, public;

-- IAM tables (canonical users system)
CREATE TABLE IF NOT EXISTS iam_users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    citizen_id UUID NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING_VERIFICATION',
    is_superuser BOOLEAN NOT NULL DEFAULT false,
    full_name VARCHAR(255),
    phone VARCHAR(50),
    department VARCHAR(255),
    position VARCHAR(255),
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    last_login_at TIMESTAMP WITH TIME ZONE NULL,
    last_login_ip VARCHAR(50) NULL,
    password_changed_at TIMESTAMP WITH TIME ZONE NULL,
    password_expires_at TIMESTAMP WITH TIME ZONE NULL,
    mfa_enabled BOOLEAN NOT NULL DEFAULT false,
    mfa_secret VARCHAR(255) NULL,
    mfa_type VARCHAR(50) NOT NULL DEFAULT 'NONE',
    custom_metadata JSONB NULL,
    deleted_at TIMESTAMP WITH TIME ZONE NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NULL,
    created_by VARCHAR(36) NULL,
    updated_by VARCHAR(36) NULL,
    is_active BOOLEAN NOT NULL DEFAULT true
);

CREATE INDEX IF NOT EXISTS ix_iam_users_status_created ON iam_users (status, created_at);
CREATE INDEX IF NOT EXISTS ix_iam_users_username_lower ON iam_users (lower(username));
CREATE INDEX IF NOT EXISTS ix_iam_users_email_lower ON iam_users (lower(email));
CREATE INDEX IF NOT EXISTS ix_iam_users_citizen_id ON iam_users (citizen_id);
CREATE INDEX IF NOT EXISTS ix_iam_users_status ON iam_users (status);

CREATE TABLE IF NOT EXISTS iam_roles (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NULL,
    role_type VARCHAR(50) NOT NULL DEFAULT 'CUSTOM',
    is_system BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NULL,
    created_by VARCHAR(36) NULL,
    updated_by VARCHAR(36) NULL,
    is_active BOOLEAN NOT NULL DEFAULT true
);

CREATE INDEX IF NOT EXISTS ix_iam_roles_name ON iam_roles (name);
CREATE INDEX IF NOT EXISTS ix_iam_roles_type ON iam_roles (role_type);

CREATE TABLE IF NOT EXISTS iam_user_roles (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES iam_users(id) ON DELETE CASCADE,
    role_id VARCHAR(36) NOT NULL REFERENCES iam_roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_by VARCHAR(36) NULL REFERENCES iam_users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NULL,
    created_by VARCHAR(36) NULL,
    updated_by VARCHAR(36) NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    UNIQUE (user_id, role_id)
);

CREATE INDEX IF NOT EXISTS ix_iam_user_roles_user_id ON iam_user_roles (user_id);
CREATE INDEX IF NOT EXISTS ix_iam_user_roles_role_id ON iam_user_roles (role_id);

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

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);

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

CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

INSERT INTO iam_roles (id, name, description, role_type, is_system, is_active)
VALUES (
    uuid_generate_v4()::text,
    'SUPERADMIN',
    'System superadmin',
    'SYSTEM',
    true,
    true
) ON CONFLICT (name) DO NOTHING;

INSERT INTO iam_users (id, username, email, password_hash, status, is_superuser, full_name, is_active)
VALUES (
    uuid_generate_v4()::text,
    'admin',
    'admin@sila.system',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq9w5GS',
    'ACTIVE',
    true,
    'SILA System Administrator',
    true
) ON CONFLICT (email) DO NOTHING;

INSERT INTO iam_user_roles (id, user_id, role_id, is_active)
VALUES (
    uuid_generate_v4()::text,
    (SELECT id FROM iam_users WHERE email = 'admin@sila.system'),
    (SELECT id FROM iam_roles WHERE name = 'SUPERADMIN'),
    true
) ON CONFLICT (user_id, role_id) DO NOTHING;

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE OR REPLACE VIEW system_stats AS
SELECT
    'users' as table_name,
    COUNT(*) as total_records,
    COUNT(CASE WHEN is_active = true THEN 1 END) as active_records,
    MAX(created_at) as last_created
FROM users;

GRANT USAGE ON SCHEMA sila_system TO sila_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA sila_system TO sila_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA sila_system TO sila_user;

DO $$
BEGIN
    RAISE NOTICE '🚀 SILA System Database initialized successfully';
END $$;
