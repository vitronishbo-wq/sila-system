"""
Citizen Educational Marketplace Module

Subsystem de educacao que implementa um marketplace nacional de oportunidades educacionais.

Arquitetura: 8 subdomínios com Hexagonal Architecture
- discovery: Descoberta de vagas e programas
- ranking: Ranking de instituições
- matching: Matching automático
- recommendation: Recomendações personalizadas
- search: Busca avançada
- booking: Reserva de vagas
- transfers: Transferências self-service
- admissions: Admissão automática
"""

__version__ = "0.1.0"
__author__ = "SILA System"
__all__ = [
    "discovery",
    "ranking",
    "matching",
    "recommendation",
    "search",
    "booking",
    "transfers",
    "admissions",
]
