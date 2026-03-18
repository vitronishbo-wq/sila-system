"""
SQL Migration for Event Store Table
This creates the event_store table required for PostgreSQL event persistence
"""
CREATE_EVENT_STORE_TABLE = '\nCREATE TABLE IF NOT EXISTS event_store (\n    event_id UUID PRIMARY KEY,\n    aggregate_id UUID NOT NULL,\n    aggregate_type VARCHAR(255) NOT NULL,\n    event_type VARCHAR(255) NOT NULL,\n    version INTEGER DEFAULT 1,\n    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,\n    event_data TEXT NOT NULL,\n    event_metadata TEXT,\n    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP\n);\n'
CREATE_INDEX_AGGREGATE_ID = 'CREATE INDEX IF NOT EXISTS ix_aggregate_id ON event_store(aggregate_id);'
CREATE_INDEX_AGGREGATE_TYPE = 'CREATE INDEX IF NOT EXISTS ix_aggregate_type ON event_store(aggregate_type);'
CREATE_INDEX_EVENT_TYPE = 'CREATE INDEX IF NOT EXISTS ix_event_type ON event_store(event_type);'
CREATE_INDEX_TIMESTAMP = 'CREATE INDEX IF NOT EXISTS ix_timestamp ON event_store(timestamp);'
CREATE_INDEX_AGGREGATE_TIMESTAMP = 'CREATE INDEX IF NOT EXISTS ix_aggregate_id_timestamp ON event_store(aggregate_id, timestamp);'
CREATE_INDEX_EVENT_TYPE_TIMESTAMP = 'CREATE INDEX IF NOT EXISTS ix_event_type_timestamp ON event_store(event_type, timestamp);'
CREATE_INDEX_AGGREGATE_TYPE_TIMESTAMP = 'CREATE INDEX IF NOT EXISTS ix_aggregate_type_timestamp ON event_store(aggregate_type, timestamp);'
CREATE_INDEXES = [CREATE_INDEX_AGGREGATE_ID, CREATE_INDEX_AGGREGATE_TYPE, CREATE_INDEX_EVENT_TYPE, CREATE_INDEX_TIMESTAMP, CREATE_INDEX_AGGREGATE_TIMESTAMP, CREATE_INDEX_EVENT_TYPE_TIMESTAMP, CREATE_INDEX_AGGREGATE_TYPE_TIMESTAMP]
CHECK_TABLE_EXISTS = "\nSELECT EXISTS (\n    SELECT 1 FROM information_schema.tables \n    WHERE table_name = 'event_store'\n);\n"
DROP_EVENT_STORE_TABLE = '\nDROP TABLE IF EXISTS event_store CASCADE;\n'
__all__ = ['CREATE_EVENT_STORE_TABLE', 'CREATE_INDEXES', 'CHECK_TABLE_EXISTS', 'DROP_EVENT_STORE_TABLE']