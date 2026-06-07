from apps.backend.app.modules.society.cultura.workers.edital_worker import EditalWorker
from apps.backend.app.modules.society.cultura.workers.outbox_worker import OutboxWorker
from apps.backend.app.modules.society.cultura.workers.patrimonio_worker import PatrimonioWorker

__all__ = ["OutboxWorker", "EditalWorker", "PatrimonioWorker"]
