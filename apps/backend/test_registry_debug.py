#!/usr/bin/env python
"""Debug script to test event registry"""

import sys

sys.path.insert(0, "/home/dev03wsl/sila-system/apps/backend")

from datetime import date
from uuid import uuid4

from apps.backend.app.infrastructure.event_sourcing.registry import EventRegistry, register_events
from apps.backend.app.modules.justice.domain.events import CitizenCreated

# Register events
print("Registering events...")
register_events()

# Check registry
print(f"\nRegistered events: {list(EventRegistry.list_registered().keys())}")

# Test deserialization
print("\nTesting deserialization...")
citizen_id = uuid4()
event = CitizenCreated(
    aggregate_id=citizen_id,
    aggregate_type="Citizen",
    event_type="CitizenCreated",
    first_name="Test",
    last_name="User",
    birth_date=date(1990, 1, 1),
    birth_place="Lisbon",
    nationality="PT",
)

print(f"Original event: {type(event).__name__}")
print(f"  - first_name: {event.first_name}")
print(f"  - event_type: {event.event_type}")

# Convert to dict and back
event_dict = event.to_dict()
print(f"\nSerialized: {event_dict}")

# Try to get from registry
event_type = event_dict.get("event_type")
event_class = EventRegistry.get(event_type)
print(f"\nLookup result for '{event_type}': {event_class}")

if event_class:
    reconstructed = event_class.from_dict(event_dict)
else:
    from apps.backend.app.core.events.domain_event import DomainEvent

    reconstructed = DomainEvent.from_dict(event_dict)

print(f"\nReconstructed event: {type(reconstructed).__name__}")
if hasattr(reconstructed, "first_name"):
    print(f"  - first_name: {reconstructed.first_name}")
else:
    print(
        f"  - Has first_name? NO (only has: {', '.join([k for k in reconstructed.__dict__.keys() if not k.startswith('_')])})"
    )
