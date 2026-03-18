"""
Módulo de Analytics sobre AuditLogs.
Foco: SLA, Anomalias e Métricas Operacionais.
Leitura e Agregação apenas. Zero efeitos colaterais.
"""
from typing import Dict, List, Any
from datetime import datetime, timedelta
import json
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import Base
audit_tbl = Base.metadata.tables.get('audit_logs')

class AuditAnalytics:

    def __init__(self, db: AsyncSession, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.db = db

    async def _get_audit_columns(self) -> set[str]:
        result = await self.db.execute(text("\n                SELECT column_name\n                FROM information_schema.columns\n                WHERE table_name = 'audit_logs'\n                "))
        return {row[0] for row in result.fetchall()}

    async def get_sla_metrics(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Calcula metricas de SLA baseadas na diferença de tempo entre eventos.
        Ex: REQUEST_CREATED -> DOCUMENT_ISSUED
        """
        if audit_tbl is None:
            res_created = await self.db.execute(text("\n                    SELECT resource_id, created_at\n                    FROM audit_logs\n                    WHERE action = 'REQUEST_CREATED'\n                      AND created_at BETWEEN :start_date AND :end_date\n                    "), {'start_date': start_date, 'end_date': end_date})
            created_map = {row[0]: row[1] for row in res_created.fetchall()}
            if not created_map:
                return {'avg_issuance_time_seconds': 0, 'total_processed': 0}
            res_issued = await self.db.execute(text("\n                    SELECT created_at, metadata_json\n                    FROM audit_logs\n                    WHERE action = 'DOCUMENT_ISSUED'\n                      AND created_at >= :start_date\n                    "), {'start_date': start_date})
            issued_rows = res_issued.fetchall()
            durations = []
            for row in issued_rows:
                payload = row[1] or {}
                if isinstance(payload, str):
                    try:
                        payload = json.loads(payload)
                    except Exception:
                        payload = {}
                if isinstance(payload, dict):
                    payload = payload.get('new_value') or payload
                if not isinstance(payload, dict) or 'request_id' not in payload:
                    continue
                req_id = payload['request_id']
                issued_at = row[0]
                if req_id in created_map:
                    created_at = created_map[req_id]
                    durations.append((issued_at - created_at).total_seconds())
            avg_time = sum(durations) / len(durations) if durations else 0
            return {'avg_issuance_time_seconds': round(avg_time, 2), 'min_issuance_time_seconds': round(min(durations), 2) if durations else 0, 'max_issuance_time_seconds': round(max(durations), 2) if durations else 0, 'total_processed': len(durations), 'sample_size': len(durations)}
        cols = await self._get_audit_columns()
        payload_col = 'new_value' if 'new_value' in cols else 'metadata_json' if 'metadata_json' in cols else None
        if payload_col is None:
            return {'avg_issuance_time_seconds': 0, 'total_processed': 0}
        q_created = select(audit_tbl.c.resource_id, audit_tbl.c.created_at).where(audit_tbl.c.action == 'REQUEST_CREATED', audit_tbl.c.created_at.between(start_date, end_date))
        res_created = await self.db.execute(q_created)
        created_map = {row[0]: row[1] for row in res_created.fetchall()}
        if not created_map:
            return {'avg_issuance_time_seconds': 0, 'total_processed': 0}
        if payload_col in audit_tbl.c:
            q_issued = select(audit_tbl.c.created_at, getattr(audit_tbl.c, payload_col)).where(audit_tbl.c.action == 'DOCUMENT_ISSUED', audit_tbl.c.created_at >= start_date)
            res_issued = await self.db.execute(q_issued)
        else:
            q_issued = text(f'\n                SELECT created_at, {payload_col}\n                FROM audit_logs\n                WHERE action = :action\n                  AND created_at >= :start_date\n                ')
            res_issued = await self.db.execute(q_issued, {'action': 'DOCUMENT_ISSUED', 'start_date': start_date})
        issued_rows = res_issued.fetchall()
        durations = []
        for row in issued_rows:
            payload = row[1] or {}
            if isinstance(payload, str):
                try:
                    payload = json.loads(payload)
                except Exception:
                    payload = {}
            if payload_col == 'metadata_json' and isinstance(payload, dict):
                payload = payload.get('new_value') or payload
            if not isinstance(payload, dict) or 'request_id' not in payload:
                continue
            req_id = payload['request_id']
            issued_at = row[0]
            if req_id in created_map:
                created_at = created_map[req_id]
                duration = (issued_at - created_at).total_seconds()
                durations.append(duration)
        avg_time = sum(durations) / len(durations) if durations else 0
        return {'avg_issuance_time_seconds': round(avg_time, 2), 'min_issuance_time_seconds': round(min(durations), 2) if durations else 0, 'max_issuance_time_seconds': round(max(durations), 2) if durations else 0, 'total_processed': len(durations), 'sample_size': len(durations)}

    async def detect_anomalies(self, lookback_minutes: int=60, threshold: int=10) -> List[Dict[str, Any]]:
        """
        Detecta picos anormais de eventos específicos (ex: REJECTED, DELETED)
        """
        if audit_tbl is None:
            cutoff = datetime.utcnow() - timedelta(minutes=lookback_minutes)
            result = await self.db.execute(text('\n                    SELECT action, COUNT(id) AS count\n                    FROM audit_logs\n                    WHERE created_at >= :cutoff\n                    GROUP BY action\n                    HAVING COUNT(id) > :threshold\n                    '), {'cutoff': cutoff, 'threshold': threshold})
            anomalies = []
            for row in result.fetchall():
                action = row[0]
                count = row[1]
                severity = 'INFO'
                if 'DELETED' in action or 'REJECTED' in action:
                    severity = 'HIGH' if count > threshold * 2 else 'MEDIUM'
                anomalies.append({'action': action, 'count': count, 'window_minutes': lookback_minutes, 'severity': severity, 'timestamp': datetime.utcnow().isoformat()})
            return anomalies
        cutoff = datetime.utcnow() - timedelta(minutes=lookback_minutes)
        query = select(audit_tbl.c.action, func.count(audit_tbl.c.id).label('count')).where(audit_tbl.c.created_at >= cutoff).group_by(audit_tbl.c.action).having(func.count(audit_tbl.c.id) > threshold)
        result = await self.db.execute(query)
        anomalies = []
        for row in result:
            action = row.action
            count = row.count
            severity = 'INFO'
            if 'DELETED' in action or 'REJECTED' in action:
                severity = 'HIGH' if count > threshold * 2 else 'MEDIUM'
            anomalies.append({'action': action, 'count': count, 'window_minutes': lookback_minutes, 'severity': severity, 'timestamp': datetime.utcnow().isoformat()})
        return anomalies

    async def get_event_timeline(self, resource_id: str) -> List[Dict[str, Any]]:
        """
        Reconstrói a linha do tempo completa de um recurso (cross-module)
        """
        if audit_tbl is None:
            return []
        cols = await self._get_audit_columns()
        details_col = 'new_value' if 'new_value' in cols else 'metadata_json' if 'metadata_json' in cols else None
        event_col = 'event_id' if 'event_id' in cols else 'NULL::text AS event_id'
        if 'actor_id' in cols:
            actor_col = 'actor_id'
        elif 'user_id' in cols:
            actor_col = 'CAST(user_id AS text) AS actor_id'
        else:
            actor_col = 'NULL::text AS actor_id'
        details_col_sql = details_col if details_col else 'NULL::jsonb AS details'
        query = text(f'\n            SELECT {event_col}, action, created_at, {actor_col}, {details_col_sql}\n            FROM audit_logs\n            WHERE resource_id = :resource_id\n            ORDER BY created_at ASC\n            ')
        result = await self.db.execute(query, {'resource_id': resource_id})
        logs = result.fetchall()
        return [{'event_id': row_dict.get('event_id'), 'action': row_dict.get('action'), 'timestamp': row_dict.get('created_at').isoformat() if row_dict.get('created_at') else None, 'actor': row_dict.get('actor_id'), 'details': row_dict.get(details_col) if details_col and details_col in row_dict else row_dict.get('details')} for row in logs for row_dict in [dict(row._mapping)]]