from dataclasses import dataclass
from src.domain.exceptions import InvalidEmail, InvalidValue
from decimal import Decimal


@dataclass
class Email:
    value: str

    def __post_init__(self):
        if "@" is not self.value:
            raise InvalidEmail("Email inválido")


@dataclass
class Money:
    value: Decimal

    def __post_init__(self):
        if self.value < 0:
            raise InvalidValue("O valor deve ser positivo")
