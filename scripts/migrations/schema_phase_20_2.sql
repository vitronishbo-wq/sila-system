CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE IF NOT EXISTS event_store (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id VARCHAR(255) NOT NULL,
    aggregate_type VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    version INTEGER NOT NULL,
    payload JSONB NOT NULL,
    event_metadata JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(aggregate_id, version)
);
CREATE TABLE IF NOT EXISTS snapshots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id VARCHAR(255) NOT NULL,
    aggregate_type VARCHAR(255) NOT NULL,
    version INTEGER NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(aggregate_id, version)
);
CREATE TABLE IF NOT EXISTS event_store_projections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    projection_name VARCHAR(255) NOT NULL,
    aggregate_id VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    version INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(projection_name, aggregate_id)
);
CREATE INDEX IF NOT EXISTS idx_event_store_aggregate_id ON event_store(aggregate_id);
CREATE INDEX IF NOT EXISTS idx_event_store_event_type ON event_store(event_type);
CREATE INDEX IF NOT EXISTS idx_event_store_created_at ON event_store(created_at);
CREATE INDEX IF NOT EXISTS idx_event_store_aggregate_version ON event_store(aggregate_id, version);
CREATE INDEX IF NOT EXISTS idx_event_store_aggregate_type ON event_store(aggregate_type);
CREATE INDEX IF NOT EXISTS idx_event_store_payload_gin ON event_store USING GIN(payload);
CREATE INDEX IF NOT EXISTS idx_snapshots_aggregate_id ON snapshots(aggregate_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_aggregate_version ON snapshots(aggregate_id, version);
CREATE INDEX IF NOT EXISTS idx_snapshots_created_at ON snapshots(created_at);
CREATE INDEX IF NOT EXISTS idx_projections_name_aggregate ON event_store_projections(projection_name, aggregate_id);
CREATE INDEX IF NOT EXISTS idx_projections_aggregate_id ON event_store_projections(aggregate_id);
CREATE INDEX IF NOT EXISTS idx_projections_name ON event_store_projections(projection_name);
CREATE INDEX IF NOT EXISTS idx_projections_data_gin ON event_store_projections USING GIN(data);
