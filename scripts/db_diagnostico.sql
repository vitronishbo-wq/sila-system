-- Diagnóstico geral do PostgreSQL e banco sila_dev

-- 1. Listar todos os bancos de dados
\l

-- 2. Conectar ao banco sila_dev
\c sila_dev

-- 3. Contar número de tabelas no schema público
SELECT COUNT(*) AS total_tabelas
FROM information_schema.tables
WHERE table_schema = 'public';

-- 4. Listar todas as tabelas
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- 5. Verificar se a tabela de usuários existe
SELECT EXISTS (
    SELECT FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'users'
) AS tabela_users_existe;

-- 6. Contar usuários cadastrados
SELECT COUNT(*) AS total_usuarios FROM users;

-- 7. Listar os primeiros usuários
SELECT id, email, name, role, is_active FROM users LIMIT 10;
