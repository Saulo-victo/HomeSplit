from pydantic import BaseModel
from decimal import Decimal
from enum import Enum


class CategoryEnum(str, Enum):
    MERCADO = 'Mercado'
    INTERNET = 'Internet'
    ALUGUEL = 'Aluguel'
    RACAO = 'Ração'
    ENERGIA = 'Energia'
    AGUA = 'Água'
    OUTROS = 'Outros'


class RequestUserRegister(BaseModel):
    name: str
    email: str


class ResponseUserRegister(BaseModel):
    id: str
    name: str
    email: str


class RequestExpenseRegister(BaseModel):
    expense_value: Decimal
    description: str
    category: CategoryEnum


class ResponseExpenseRegister(BaseModel):
    id: str
    expense_value: float
    description: str
    date: str
    category: CategoryEnum
    id_user: str
