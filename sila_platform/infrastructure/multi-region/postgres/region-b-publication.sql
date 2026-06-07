-- Regiao B (Benguela) - publicacao logica reversa (ativo-ativo)
CREATE PUBLICATION op_publication_b FOR TABLE
  op_outbox_events,
  op_outbox_event_consumption,
  op_sagas,
  op_dashboard_read,
  op_dashboard_projection_offsets,
  op_event_store,
  event_catalog;
