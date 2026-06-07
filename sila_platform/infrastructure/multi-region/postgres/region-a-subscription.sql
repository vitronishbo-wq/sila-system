-- Regiao A (Luanda) - assinatura da publicacao da Regiao B
CREATE SUBSCRIPTION op_subscription_from_b
CONNECTION 'host=region-b-db user=replicator password=change-me dbname=op'
PUBLICATION op_publication_b
WITH (create_slot = true, enabled = true);
