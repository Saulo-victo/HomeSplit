from dataclasses import dataclass
from src.domain.value_objects import Email, Money
import datetime


@dataclass
class User:
    id: str
    name: str
    email: Email


@dataclass
class Expense:
    id: str
    expense_value: Money
    description: str
    date: datetime
    category: str
    id_user: str


@dataclass
class ExpenseWithUserName:
    id: str
    expense_value: Money
    description: str
    date: datetime
    category: str
    id_user: str
    name_user: str
