-- PHASE 20.2: EVENT SOURCING TEST DATA
INSERT INTO event_store (aggregate_id, aggregate_type, event_type, version, payload, event_metadata)
VALUES
  ('user_100', 'USER', 'UserCreated', 1, 
   '{\
