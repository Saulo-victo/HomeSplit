from abc import ABC, abstractmethod
from src.domain.value_objects import Money
import datetime
from src.domain.entities import User, Expense


class IUserRepository(ABC):
    @abstractmethod
    def save_user(self, user_id: str, name: str, email: str) -> User:
        pass

    @abstractmethod
    def get_all_users(self, user_email) -> list[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, search_id) -> User:
        pass


class IExpenseRepository(ABC):
    @abstractmethod
    def save_expense(self, value: Money, description: str, date: datetime, category: str) -> Expense:
        pass

    @abstractmethod
    def filter_by_category(self, category: str) -> list[Expense]:
        pass


class IUnitOfWork(ABC):
    @abstractmethod
    def __enter__(self) -> None:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc, tb) -> None:
        pass
