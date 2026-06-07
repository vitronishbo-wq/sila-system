from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession


class TimelineService:
    """Builds timeline from real audit events instead of hardcoded steps."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_timeline(self, resource_id: str) -> list[dict[str, Any]]:
        result = await self.session.execute(
            text("""
                SELECT action, created_at, metadata_json
                FROM audit_logs
                WHERE resource_id = :resource_id
                ORDER BY created_at ASC
            """),
            {"resource_id": resource_id},
        )
        rows = result.fetchall()
        if not rows:
            return []

        return [
            {
                "etapa": self._action_to_etapa(row[0]),
                "data_hora": row[1].isoformat() if row[1] else None,
                "concluido": True,
                "evento": row[0],
            }
            for row in rows
        ]

    async def get_wizard_timeline(self, wizard_id: str) -> list[dict[str, Any]]:
        """Get timeline for a wizard session from its events."""
        events = []
        base_events = [
            {"etapa": "Pedido criado", "evento": "pedido_criado"},
            {"etapa": "Dados do estudante", "evento": "dados_estudante"},
            {"etapa": "Dados do encarregado", "evento": "dados_encarregado"},
            {"etapa": "Selecao de escola", "evento": "selecao_escola"},
            {"etapa": "Documentos enviados", "evento": "documentos_enviados"},
            {"etapa": "Elegibilidade verificada", "evento": "elegibilidade_verificada"},
            {"etapa": "Reserva efetuada", "evento": "vaga_reservada"},
            {"etapa": "Pagamento confirmado", "evento": "pagamento_confirmado"},
            {"etapa": "Matricula criada", "evento": "matricula_criada"},
            {"etapa": "Concluido", "evento": "concluido"},
        ]
        for ev in base_events:
            audit_result = await self.session.execute(
                text("""
                    SELECT created_at FROM audit_logs
                    WHERE resource_id = :resource_id AND action = :action
                    ORDER BY created_at DESC LIMIT 1
                """),
                {"resource_id": wizard_id, "action": ev["evento"]},
            )
            row = audit_result.fetchone()
            events.append({
                "etapa": ev["etapa"],
                "data_hora": row[0].isoformat() if row else None,
                "concluido": row is not None,
                "evento": ev["evento"],
            })
        return events

    @staticmethod
    def _action_to_etapa(action: str) -> str:
        mapping = {
            "vaga_reservada": "Reserva de vaga",
            "vaga_confirmada": "Vaga confirmada",
            "vaga_expirada": "Reserva expirada",
            "vaga_cancelada": "Reserva cancelada",
            "matricula_criada": "Matricula criada",
            "enrollment_created": "Matricula criada",
            "enrollment_completed": "Matricula concluida",
            "transferencia_iniciada": "Transferencia iniciada",
            "transferencia_concluida": "Transferencia concluida",
            "pedido_criado": "Pedido criado",
            "dados_estudante": "Dados do estudante",
            "dados_encarregado": "Dados do encarregado",
            "selecao_escola": "Selecao de escola",
            "documentos_enviados": "Documentos enviados",
            "elegibilidade_verificada": "Elegibilidade verificada",
            "pagamento_confirmado": "Pagamento confirmado",
            "concluido": "Concluido",
        }
        return mapping.get(action, action)
