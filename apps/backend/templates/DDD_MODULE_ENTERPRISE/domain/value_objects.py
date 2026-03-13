from dataclasses import dataclass

@dataclass(frozen=True)
class {{ value_object_name }}:
    valor: str

    def __post_init__(self):
        if not self.valor:
            raise ValueError("Valor não pode ser vazio")
