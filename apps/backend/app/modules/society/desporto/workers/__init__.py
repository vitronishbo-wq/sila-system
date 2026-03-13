from app.modules.society.desporto.workers.estatistica_worker import EstatisticaWorker
from app.modules.society.desporto.workers.notificacao_worker import NotificacaoWorker
from app.modules.society.desporto.workers.outbox_worker import OutboxWorker
from app.modules.society.desporto.workers.ranking_worker import RankingWorker
__all__ = ['OutboxWorker', 'RankingWorker', 'EstatisticaWorker', 'NotificacaoWorker']