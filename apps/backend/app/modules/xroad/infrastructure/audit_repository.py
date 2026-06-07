import json
import os

from apps.backend.app.modules.xroad.domain.audit_log import AuditEntry


class ImmutableAuditRepository:
    def __init__(self, log_file: str = "storage/logs/xroad_audit.chain"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def append(self, entry: AuditEntry):
        with open(self.log_file, "a") as f:
            f.write(entry.model_dump_json() + "\n")

    def get_last_hash(self) -> str:
        if not os.path.exists(self.log_file) or os.stat(self.log_file).st_size == 0:
            return "0"
        try:
            with open(self.log_file) as f:
                lines = f.readlines()
                if not lines:
                    return "0"
                last_line = lines[-1].strip()
                if not last_line:
                    return "0"
                entry_data = json.loads(last_line)
                last_entry = AuditEntry(**entry_data)
                return last_entry.compute_hash()
        except (IndexError, json.JSONDecodeError):
            return "0"
