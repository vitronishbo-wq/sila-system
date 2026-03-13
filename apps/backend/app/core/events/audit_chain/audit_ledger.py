from app.core.events.audit_chain.hash_chain import calculate_hash

class AuditLedger:

    def __init__(self):
        self.chain = []

    def append(self, event):
        if isinstance(event, dict):
            event_id = event.get('id') or event.get('event_id')
            event_name = event.get('name') or event.get('event_name')
        else:
            event_id = getattr(event, 'id', None)
            event_name = getattr(event, 'name', None)
        previous_hash = self.chain[-1]['hash'] if self.chain else '0'
        record = {'event_id': event_id, 'event_name': event_name, 'previous_hash': previous_hash}
        record['hash'] = calculate_hash(record)
        self.chain.append(record)