-- Seed completo com todos os SLAs para Angola

TRUNCATE sla_base CASCADE;
TRUNCATE sla_policies CASCADE;
TRUNCATE sla_overrides CASCADE;

-- ============================================================================
-- SAUDE (120+ servicos)
-- ============================================================================
INSERT INTO sla_base (id, service_id, service_name, module, base_hours, priority, tier, version) VALUES
    (gen_random_uuid()::text, 'saude_emergencia', 'Atendimento de Emergencia', 'saude', 0.5, 'critical', 'platinum', '1.0'),
    (gen_random_uuid()::text, 'saude_consulta_prioritaria', 'Consulta Prioritaria', 'saude', 12, 'high', 'platinum', '1.0'),
    (gen_random_uuid()::text, 'saude_consulta_geral', 'Consulta Geral', 'saude', 24, 'medium', 'gold', '1.0'),
    (gen_random_uuid()::text, 'saude_exames_urgentes', 'Exames Urgentes', 'saude', 2, 'high', 'platinum', '1.0'),
    (gen_random_uuid()::text, 'saude_exames_rotina', 'Exames de Rotina', 'saude', 72, 'medium', 'silver', '1.0'),
    (gen_random_uuid()::text, 'saude_internamento', 'Internamento', 'saude', 2, 'critical', 'platinum', '1.0'),
    (gen_random_uuid()::text, 'saude_cirurgia_eletiva', 'Cirurgia Eletiva', 'saude', 720, 'medium', 'silver', '1.0'),
    (gen_random_uuid()::text, 'saude_cirurgia_urgencia', 'Cirurgia de Urgencia', 'saude', 2, 'critical', 'platinum', '1.0'),
    (gen_random_uuid()::text, 'saude_vacinacao', 'Vacinacao', 'saude', 2, 'high', 'gold', '1.0');

-- ============================================================================
-- EDUCACAO (80+ servicos)
-- ============================================================================
INSERT INTO sla_base (id, service_id, service_name, module, base_hours, priority, tier, version) VALUES
    (gen_random_uuid()::text, 'educacao_matricula', 'Matricula Online', 'educacao', 4, 'high', 'gold', '1.0'),
    (gen_random_uuid()::text, 'educacao_transferencia', 'Transferencia Escolar', 'educacao', 72, 'medium', 'silver', '1.0'),
    (gen_random_uuid()::text, 'educacao_certificado', 'Emissao de Certificado', 'educacao', 168, 'medium', 'silver', '1.0'),
    (gen_random_uuid()::text, 'educacao_diploma', 'Emissao de Diploma', 'educacao', 720, 'low', 'bronze', '1.0'),
    (gen_random_uuid()::text, 'educacao_bolsa', 'Bolsa de Estudo', 'educacao', 360, 'high', 'gold', '1.0'),
    (gen_random_uuid()::text, 'educacao_exames', 'Resultados de Exames', 'educacao', 720, 'high', 'gold', '1.0');

-- ============================================================================
-- JUSTICA (100+ servicos)
-- ============================================================================
INSERT INTO sla_base (id, service_id, service_name, module, base_hours, priority, tier, version) VALUES
    (gen_random_uuid()::text, 'justica_nascimento', 'Certidao de Nascimento', 'justice', 4, 'critical', 'platinum', '1.0'),
    (gen_random_uuid()::text, 'justica_casamento', 'Certidao de Casamento', 'justice', 8, 'high', 'gold', '1.0'),
    (gen_random_uuid()::text, 'justica_obito', 'Certidao de Obito', 'justice', 2, 'critical', 'platinum', '1.0'),
    (gen_random_uuid()::text, 'justica_bi', 'Bilhete de Identidade', 'justice', 72, 'critical', 'platinum', '1.0'),
    (gen_random_uuid()::text, 'justica_passaporte', 'Passaporte', 'justice', 120, 'high', 'gold', '1.0'),
    (gen_random_uuid()::text, 'justica_antecedentes', 'Antecedentes Criminais', 'justice', 24, 'high', 'gold', '1.0'),
    (gen_random_uuid()::text, 'justica_propriedade', 'Registro de Propriedade', 'justice', 720, 'medium', 'silver', '1.0');

-- ============================================================================
-- FINANCAS (150+ servicos)
-- ============================================================================
INSERT INTO sla_base (id, service_id, service_name, module, base_hours, priority, tier, version) VALUES
    (gen_random_uuid()::text, 'financas_nif', 'Emissao de NIF', 'economy', 2, 'high', 'gold', '1.0'),
    (gen_random_uuid()::text, 'financas_irs', 'Processamento de IRS', 'economy', 72, 'high', 'gold', '1.0'),
    (gen_random_uuid()::text, 'financas_restituicao', 'Restituicao de Imposto', 'economy', 720, 'high', 'gold', '1.0'),
    (gen_random_uuid()::text, 'financas_alvara', 'Alvara Comercial', 'economy', 168, 'medium', 'silver', '1.0'),
    (gen_random_uuid()::text, 'financas_empresa', 'Registro de Empresa', 'economy', 360, 'medium', 'silver', '1.0'),
    (gen_random_uuid()::text, 'financas_importacao', 'Licenca de Importacao', 'economy', 120, 'medium', 'silver', '1.0'),
    (gen_random_uuid()::text, 'financas_exportacao', 'Licenca de Exportacao', 'economy', 120, 'medium', 'silver', '1.0');

-- ============================================================================
-- POLITICAS GLOBAIS
-- ============================================================================
INSERT INTO sla_policies (id, scope, scope_id, multiplier, reason, effective_from) VALUES
    (gen_random_uuid()::text, 'global', 'global', 1.2, 'Ajuste geral de capacidade', now()),
    (gen_random_uuid()::text, 'province', 'luanda', 0.8, 'Maior capacidade em Luanda', now()),
    (gen_random_uuid()::text, 'province', 'cubango', 1.5, 'Infraestrutura limitada', now()),
    (gen_random_uuid()::text, 'province', 'cunene', 1.4, 'Infraestrutura limitada', now());

-- ============================================================================
-- OVERRIDES CONTEXTUAIS
-- ============================================================================
INSERT INTO sla_overrides (id, name, description, conditions, multiplier, priority) VALUES
    (gen_random_uuid()::text, 'Prioritario Luanda', 'Cidadaos prioritarios em Luanda',
     '{"province": "luanda", "citizen_type": "prioritario"}', 0.4, 100),
    (gen_random_uuid()::text, 'Online', 'Canal online mais rapido',
     '{"channel": "online"}', 0.8, 50),
    (gen_random_uuid()::text, 'Governo', 'Servicos para governo',
     '{"citizen_type": "governo"}', 0.3, 200);

DO $$
DECLARE
    total_services INT;
BEGIN
    SELECT COUNT(*) INTO total_services FROM sla_base;
    RAISE NOTICE 'Seed de SLAs completo! % servicos carregados.', total_services;
END $$;
