"""
Reports Module Models - Architectural Decision Documentation

DECISÃO ARQUITETURAL: O módulo 'reports' NÃO possui modelos de banco de dados próprios.

JUSTIFICATIVA:
=============
O módulo 'reports' é estritamente um módulo de SERVIÇO/TRANSFORMAÇÃO que:
- Não cria ou armazena dados persistentemente
- Apenas lê e transforma dados existentes de outros módulos (users, clients, transactions, etc.)
- Gera saídas em formato PDF, JSON, CSV ou outros formatos
- Não requer agendamento, auditoria ou controle de estado

MODELOS NÃO NECESSÁRIOS:
=======================
- Report: Não precisamos rastrear relatórios individuais
- ReportSchedule: Não há necessidade de agendamento (relatórios são gerados on-demand)
- ReportLog: Não precisamos de auditoria específica (logs gerais são suficientes)

SE NECESSIDADE FUTURA SURGIR:
============================
Se houver requisitos futuros que exijam:
- Agendamento automático de relatórios
- Controle de estado de geração
- Auditoria específica de relatórios

ENTÃO implementar:
- ReportSchedule (para agendamento)
- ReportExecution (para controle de execução)
- ReportLog (para auditoria específica)

ATÉ LÁ: Manter abordagem enxuta atual.
"""

# Este módulo existe apenas para documentar a decisão arquitetural
# Não há modelos ativos implementados
