-- PHASE 20.2 SEED DATA
INSERT INTO institutions (id, name, code, status, created_at) VALUES (1, "Instituição Teste", "INST_TEST", "ACTIVE", NOW()) ON CONFLICT DO NOTHING;
INSERT INTO users (id, username, email, full_name, status, created_at) VALUES (100, "user_test", "user@test.com", "User Test", "ACTIVE", NOW()), (101, "admin_test", "admin@test.com", "Admin Test", "ACTIVE", NOW()), (102, "readonly_test", "readonly@test.com", "ReadOnly Test", "ACTIVE", NOW()) ON CONFLICT DO NOTHING;
INSERT INTO roles (id, name, description, status) VALUES (10, "ADMIN", "Administrator", "ACTIVE"), (11, "USER", "Standard User", "ACTIVE"), (12, "READONLY", "Read-Only Access", "ACTIVE") ON CONFLICT DO NOTHING;
