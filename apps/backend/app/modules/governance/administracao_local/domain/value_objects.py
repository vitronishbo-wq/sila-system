from dataclasses import dataclass


@dataclass(frozen=True)
class CodigoAdministrativo:
    valor: str

    def __post_init__(self):
        if not self.valor:
            raise ValueError("Código administrativo não pode ser vazio")
