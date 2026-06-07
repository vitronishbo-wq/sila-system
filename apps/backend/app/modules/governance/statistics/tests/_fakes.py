def metrica_payload() -> dict:
    return {
        "nome": "taxa_emprego",
        "descricao": "Taxa de emprego formal",
        "tipo": "porcentagem",
        "unidade": "%",
        "fonte_dados": "emprego",
        "periodicidade": "mensal",
    }


def kpi_payload(metrica_id: int) -> dict:
    return {
        "nome": "kpi_emprego",
        "descricao": "KPI de emprego",
        "metrica_id": metrica_id,
        "valor_alvo": 70.0,
        "unidade": "%",
        "peso": 2.0,
        "limite_inferior": 50.0,
        "limite_superior": 100.0,
    }


def named_payload(nome: str = "item") -> dict:
    return {"nome": nome, "descricao": f"descricao {nome}", "conteudo": {"chave": "valor"}}
