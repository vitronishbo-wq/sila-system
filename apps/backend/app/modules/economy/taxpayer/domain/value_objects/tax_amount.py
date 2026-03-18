"""TaxAmount Value Object - Valor Fiscal com Precisão Decimal"""
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Union

@dataclass(frozen=True)
class TaxAmount:
    """
    Value Object para valores fiscais com precisão decimal.
    
    Garante que:
    - Valores nunca podem ser negativos
    - Sempre usa Decimal para precisão (não float)
    - Suporta operações aritméticas básicas
    - Armazena a moeda (padrão: AOA - Kwanza Angolano)
    """
    value: Decimal
    currency: str = 'AOA'

    def __post_init__(self) -> None:
        """Valida o valor no momento da instanciação."""
        if self.value < Decimal('0'):
            raise ValueError('Valor da taxa não pode ser negativo')
        if not isinstance(self.value, Decimal):
            object.__setattr__(self, 'value', Decimal(str(self.value)))

    @classmethod
    def from_float(cls, value: float, currency: str='AOA') -> 'TaxAmount':
        """
        Cria TaxAmount a partir de um float.
        
        Args:
            value: Valor em float
            currency: Código da moeda (padrão: AOA)
            
        Returns:
            Instância de TaxAmount com Decimal interno
            
        Raises:
            ValueError: Se o valor for negativo
        """
        try:
            decimal_value = Decimal(str(value))
            return cls(value=decimal_value, currency=currency)
        except (InvalidOperation, ValueError) as e:
            raise ValueError(f'Valor inválido: {value}') from e

    @classmethod
    def from_string(cls, value: str, currency: str='AOA') -> 'TaxAmount':
        """
        Cria TaxAmount a partir de uma string.
        
        Args:
            value: Valor em string (ex: "1500.50")
            currency: Código da moeda (padrão: AOA)
            
        Returns:
            Instância de TaxAmount
            
        Raises:
            ValueError: Se o formato for inválido
        """
        try:
            decimal_value = Decimal(value.strip())
            return cls(value=decimal_value, currency=currency)
        except (InvalidOperation, ValueError) as e:
            raise ValueError(f'Valor inválido: {value}') from e

    def __add__(self, other: Union['TaxAmount', Decimal, float, int]) -> 'TaxAmount':
        """Soma dois valores de taxa."""
        if isinstance(other, TaxAmount):
            if self.currency != other.currency:
                raise ValueError(f'Não é possível somar moedas diferentes: {self.currency} e {other.currency}')
            return TaxAmount(self.value + other.value, self.currency)
        decimal_other = Decimal(str(other))
        return TaxAmount(self.value + decimal_other, self.currency)

    def __sub__(self, other: Union['TaxAmount', Decimal, float, int]) -> 'TaxAmount':
        """Subtrai dois valores de taxa."""
        if isinstance(other, TaxAmount):
            if self.currency != other.currency:
                raise ValueError(f'Não é possível subtrair moedas diferentes: {self.currency} e {other.currency}')
            result = self.value - other.value
            if result < 0:
                raise ValueError('Resultado não pode ser negativo')
            return TaxAmount(result, self.currency)
        decimal_other = Decimal(str(other))
        result = self.value - decimal_other
        if result < 0:
            raise ValueError('Resultado não pode ser negativo')
        return TaxAmount(result, self.currency)

    def __mul__(self, factor: Union[Decimal, float, int]) -> 'TaxAmount':
        """Multiplica o valor da taxa por um fator."""
        decimal_factor = Decimal(str(factor))
        if decimal_factor < 0:
            raise ValueError('Multiplicador não pode ser negativo')
        return TaxAmount(self.value * decimal_factor, self.currency)

    def __truediv__(self, divisor: Union[Decimal, float, int]) -> 'TaxAmount':
        """Divide o valor da taxa por um divisor."""
        decimal_divisor = Decimal(str(divisor))
        if decimal_divisor == 0:
            raise ValueError('Divisor não pode ser zero')
        if decimal_divisor < 0:
            raise ValueError('Divisor não pode ser negativo')
        return TaxAmount(self.value / decimal_divisor, self.currency)

    def __lt__(self, other: 'TaxAmount') -> bool:
        """Compara se este valor é menor que outro."""
        if not isinstance(other, TaxAmount):
            raise TypeError(f'Não é possível comparar com {type(other)}')
        if self.currency != other.currency:
            raise ValueError('Não é possível comparar moedas diferentes')
        return self.value < other.value

    def __le__(self, other: 'TaxAmount') -> bool:
        """Compara se este valor é menor ou igual a outro."""
        if not isinstance(other, TaxAmount):
            raise TypeError(f'Não é possível comparar com {type(other)}')
        if self.currency != other.currency:
            raise ValueError('Não é possível comparar moedas diferentes')
        return self.value <= other.value

    def __gt__(self, other: 'TaxAmount') -> bool:
        """Compara se este valor é maior que outro."""
        if not isinstance(other, TaxAmount):
            raise TypeError(f'Não é possível comparar com {type(other)}')
        if self.currency != other.currency:
            raise ValueError('Não é possível comparar moedas diferentes')
        return self.value > other.value

    def __ge__(self, other: 'TaxAmount') -> bool:
        """Compara se este valor é maior ou igual a outro."""
        if not isinstance(other, TaxAmount):
            raise TypeError(f'Não é possível comparar com {type(other)}')
        if self.currency != other.currency:
            raise ValueError('Não é possível comparar moedas diferentes')
        return self.value >= other.value

    def __eq__(self, other: object) -> bool:
        """Verifica igualdade de valores e moeda."""
        if not isinstance(other, TaxAmount):
            return False
        return self.value == other.value and self.currency == other.currency

    def __str__(self) -> str:
        """Retorna representação formatada como string."""
        formatted_value = f'{self.value:.2f}'
        return f'{formatted_value} {self.currency}'

    def __repr__(self) -> str:
        """Representação para debug."""
        return f'TaxAmount({self.value} {self.currency})'

    @property
    def is_zero(self) -> bool:
        """Retorna True se o valor é zero."""
        return self.value == Decimal('0')

    @property
    def is_positive(self) -> bool:
        """Retorna True se o valor é positivo."""
        return self.value > Decimal('0')

    def to_float(self) -> float:
        """Converte para float (use com cuidado - pode perder precisão)."""
        return float(self.value)

    def to_int(self) -> int:
        """Converte para inteiro (trunca casas decimais)."""
        return int(self.value)

    def round(self, places: int=2) -> 'TaxAmount':
        """
        Arredonda o valor para o número de casas decimais especificado.
        
        Args:
            places: Número de casas decimais (padrão: 2)
            
        Returns:
            Novo TaxAmount com valor arredondado
        """
        quantize_exp = Decimal(10) ** (-places)
        rounded_value = self.value.quantize(quantize_exp)
        return TaxAmount(rounded_value, self.currency)