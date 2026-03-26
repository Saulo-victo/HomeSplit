from src.domain.interfaces import IUnitOfWork
from src.domain.entities import Expense
from src.domain.value_objects import Money
from datetime import datetime
import uuid
from src.domain.exceptions import UserNotFound


class AddExpense:
    def __init__(self, repository: IUnitOfWork):
        self.uow = repository

    def execute(self, expense_data, id_user_register):
        with self.uow as uow:
            try:
                user_register = self.uow.user.get_user_by_id(id_user_register)
            except:
                raise UserNotFound("Usuário não encontrado")
            expense = Expense(
                id=str(uuid.uuid4()),
                expense_value=Money(expense_data.expense_value),
                description=expense_data.description,
                date=datetime.now(),
                category=expense_data.category.value,
                id_user=user_register.id
            )
            uow.expense.save_expense(expense)
            return expense
