import datetime


class NationalLogger:
    def __init__(self):
        self.logs = []

    def log(self, service, level, message):
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "service": service,
            "level": level,
            "message": message,
        }
        self.logs.append(entry)
        return entry

    def get_logs(self):
        return self.logs
