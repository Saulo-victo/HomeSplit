from pydantic import BaseModel
from decimal import Decimal
from enum import Enum
from fastapi.security import OAuth2


class CategoryEnum(str, Enum):
    MERCADO = 'Mercado'
    INTERNET = 'Internet'
    ALUGUEL = 'Aluguel'
    PETS = 'Pets'
    ENERGIA = 'Energia'
    AGUA = 'Água'
    MANUTENCAO = 'Manutenção'
    OUTROS = 'Outros'


class RequestUserRegister(BaseModel):
    name: str
    email: str
    password: str


class ResponseUser(BaseModel):
    id: str
    name: str
    email: str


class RequestExpenseRegister(BaseModel):
    expense_value: Decimal
    date: str
    description: str
    category: CategoryEnum


class ResponseExpense(BaseModel):
    id: str
    expense_value: float
    description: str
    date: str
    category: CategoryEnum
    id_user: str

    class Config:
        from_attributes = True


class ResponseExpenseWithNameUser(BaseModel):
    id: str
    expense_value: float
    description: str
    date: str
    category: CategoryEnum
    id_user: str
    name_user: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ResponseExpenseSumary(BaseModel):
    total_spend: Decimal
    top_category: str
    top_value_category: Decimal
    total_by_category: dict
    total_by_week: dict
    list_expenses: list
