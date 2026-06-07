from apps.backend.app.modules.society.desporto.workers.estatistica_worker import EstatisticaWorker
from apps.backend.app.modules.society.desporto.workers.notificacao_worker import NotificacaoWorker
from apps.backend.app.modules.society.desporto.workers.outbox_worker import OutboxWorker
from apps.backend.app.modules.society.desporto.workers.ranking_worker import RankingWorker

__all__ = ["OutboxWorker", "RankingWorker", "EstatisticaWorker", "NotificacaoWorker"]
