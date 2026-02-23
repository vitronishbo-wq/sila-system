"""
Módulo de Analytics sobre AuditLogs.
Foco: SLA, Anomalias e Métricas Operacionais.
Leitura e Agregação apenas. Zero efeitos colaterais.
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base

# Use core table access for audit analytics to avoid depending on ORM
# instrumentation state during test collection/import ordering.
audit_tbl = Base.metadata.tables.get("audit_logs")

class AuditAnalytics:
    
    def __init__(self, db: AsyncSession, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)
        self.db = db

    async def get_sla_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Calcula metricas de SLA baseadas na diferença de tempo entre eventos.
        Ex: REQUEST_CREATED -> DOCUMENT_ISSUED
        """
        # 1. Buscar eventos de Criação de Pedido e Emissão de Documento
        # Isso é uma simplificação. Em um sistema real com milhões de linhas,
        # isso seria feito via ETL ou Materialized View.
        # Aqui fazemos via query direta para manter simplicidade e sem novas tabelas.
        
        # Query Created Events
        if audit_tbl is None:
            return {"avg_issuance_time_seconds": 0, "total_processed": 0}

        q_created = select(
            audit_tbl.c.resource_id,
            audit_tbl.c.created_at,
        ).where(
            audit_tbl.c.action == "REQUEST_CREATED",
            audit_tbl.c.created_at.between(start_date, end_date),
        )
        res_created = await self.db.execute(q_created)
        created_map = {row[0]: row[1] for row in res_created.fetchall()}
        
        if not created_map:
             return {"avg_issuance_time_seconds": 0, "total_processed": 0}

        # Query Issued Events for the same resources
        q_issued = select(
            audit_tbl.c.created_at,
            audit_tbl.c.new_value,
        ).where(
            audit_tbl.c.action == "DOCUMENT_ISSUED",
            audit_tbl.c.created_at >= start_date,
        )
        res_issued = await self.db.execute(q_issued)
        issued_rows = res_issued.fetchall()
        
        durations = []
        for row in issued_rows:
            # row: (created_at, new_value)
            new_value = row[1]
            if not new_value or 'request_id' not in new_value:
                continue
                
            req_id = new_value['request_id']
            issued_at = row[0]
            
            if req_id in created_map:
                created_at = created_map[req_id]
                duration = (issued_at - created_at).total_seconds()
                durations.append(duration)
        
        avg_time = sum(durations) / len(durations) if durations else 0
        
        return {
            "avg_issuance_time_seconds": round(avg_time, 2),
            "min_issuance_time_seconds": round(min(durations), 2) if durations else 0,
            "max_issuance_time_seconds": round(max(durations), 2) if durations else 0,
            "total_processed": len(durations),
            "sample_size": len(durations)
        }

    async def detect_anomalies(self, lookback_minutes: int = 60, threshold: int = 10) -> List[Dict[str, Any]]:
        """
        Detecta picos anormais de eventos específicos (ex: REJECTED, DELETED)
        """
        cutoff = datetime.utcnow() - timedelta(minutes=lookback_minutes)
        
        # Agrupar por action
        query = select(
            audit_tbl.c.action,
            func.count(audit_tbl.c.id).label('count')
        ).where(
            audit_tbl.c.created_at >= cutoff
        ).group_by(
            audit_tbl.c.action
        ).having(
            func.count(audit_tbl.c.id) > threshold
        )
        
        result = await self.db.execute(query)
        anomalies = []
        
        for row in result:
            action = row.action
            count = row.count
            
            # Regras simples de anomalia (hardcoded policies por enquanto)
            severity = "INFO"
            if "DELETED" in action or "REJECTED" in action:
                severity = "HIGH" if count > threshold * 2 else "MEDIUM"
                
            anomalies.append({
                "action": action,
                "count": count,
                "window_minutes": lookback_minutes,
                "severity": severity,
                "timestamp": datetime.utcnow().isoformat()
            })
            
        return anomalies

    async def get_event_timeline(self, resource_id: str) -> List[Dict[str, Any]]:
        """
        Reconstrói a linha do tempo completa de um recurso (cross-module)
        """
        query = select(audit_tbl).where(
            audit_tbl.c.resource_id == resource_id
        ).order_by(audit_tbl.c.created_at.asc())

        result = await self.db.execute(query)
        logs = result.fetchall()

        return [
            {
                "event_id": row_dict.get("event_id"),
                "action": row_dict.get("action"),
                "timestamp": row_dict.get("created_at").isoformat() if row_dict.get("created_at") else None,
                "actor": row_dict.get("actor_id"),
                "details": row_dict.get("new_value"),
            }
            for row in logs
            for row_dict in [dict(row._mapping)]
        ]
