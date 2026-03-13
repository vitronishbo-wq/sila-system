from __future__ import annotations
from datetime import date

def next_codigo(prefixo: str, total_atual: int) -> str:
    ano = date.today().year
    return f'{prefixo}/{ano}/{total_atual + 1:05d}'