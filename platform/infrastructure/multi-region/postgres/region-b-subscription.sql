-- Regiao B (Benguela) - assinatura da publicacao da Regiao A
CREATE SUBSCRIPTION op_subscription_from_a
CONNECTION 'host=region-a-db user=replicator password=change-me dbname=op'
PUBLICATION op_publication
WITH (create_slot = true, enabled = true);
