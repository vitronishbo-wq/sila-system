from ...domain.exceptions import RegistoDuplicadoError, RegistoNaoEncontradoError
from ...domain.models import (
    RegistoCasamento,
    RegistoNascimento,
    RegistoObito,
    RegistoStatus,
)


class RegistoCivilService:
    def __init__(self):
        self._nascimentos: dict[str, RegistoNascimento] = {}
        self._obitos: dict[str, RegistoObito] = {}
        self._casamentos: dict[str, RegistoCasamento] = {}

    async def registar_nascimento(self, registo: RegistoNascimento) -> RegistoNascimento:
        if str(registo.id) in self._nascimentos:
            raise RegistoDuplicadoError(f"Nascimento {registo.id} ja registado")
        registo.status = RegistoStatus.CONCLUIDO
        registo.created_at = __import__("datetime").datetime.utcnow()
        self._nascimentos[str(registo.id)] = registo
        return registo

    async def consultar_nascimento(self, registo_id: str) -> RegistoNascimento:
        registo = self._nascimentos.get(registo_id)
        if not registo:
            raise RegistoNaoEncontradoError(registo_id)
        return registo

    async def registar_obito(self, registo: RegistoObito) -> RegistoObito:
        if str(registo.id) in self._obitos:
            raise RegistoDuplicadoError(f"Obito {registo.id} ja registado")
        registo.status = RegistoStatus.CONCLUIDO
        registo.created_at = __import__("datetime").datetime.utcnow()
        self._obitos[str(registo.id)] = registo
        return registo

    async def consultar_obito(self, registo_id: str) -> RegistoObito:
        registo = self._obitos.get(registo_id)
        if not registo:
            raise RegistoNaoEncontradoError(registo_id)
        return registo

    async def registar_casamento(self, registo: RegistoCasamento) -> RegistoCasamento:
        if str(registo.id) in self._casamentos:
            raise RegistoDuplicadoError(f"Casamento {registo.id} ja registado")
        registo.status = RegistoStatus.CONCLUIDO
        registo.created_at = __import__("datetime").datetime.utcnow()
        self._casamentos[str(registo.id)] = registo
        return registo

    async def consultar_casamento(self, registo_id: str) -> RegistoCasamento:
        registo = self._casamentos.get(registo_id)
        if not registo:
            raise RegistoNaoEncontradoError(registo_id)
        return registo
