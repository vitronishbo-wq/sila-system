from __future__ import annotations
from uuid import UUID
from app.modules.infrastructure_sector.gestao_fundiaria.application.ports.justica_service_port import JusticaServicePort

class JusticaServiceAdapter(JusticaServicePort):

    async def possui_litigio_ativo(self, imovel_id: UUID) -> bool:
        return False

    async def validar_matricula(self, numero_matricula: str, cartorio_nome: str, livro: str, folha: str) -> bool:
        _ = (numero_matricula, cartorio_nome, livro, folha)
        return True