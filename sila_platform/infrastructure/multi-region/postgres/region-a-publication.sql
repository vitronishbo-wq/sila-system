-- Regiao A (Luanda) - publicacao logica
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'change-me';

CREATE PUBLICATION op_publication FOR TABLE
  op_outbox_events,
  op_outbox_event_consumption,
  op_sagas,
  op_dashboard_read,
  op_dashboard_projection_offsets,
  op_event_store,
  event_catalog;
