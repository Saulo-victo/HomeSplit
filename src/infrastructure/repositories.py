from src.domain.entities import User, Expense
from sqlalchemy.orm import Session
from src.domain.interfaces import IExpenseRepository, IUserRepository
from decimal import Decimal
from src.infrastructure.models import UserModel, ExpenseModel


class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def save_user(self, user: User) -> None:
        db_user = UserModel(
            id=str(user.id),
            name=str(user.name),
            email=str(user.email)
        )
        self.session.add(db_user)
        self.session.commit()

    def get_all_users(self):
        users_list = []
        model_users = self.session.query(UserModel).all()
        for user in model_users:
            select_user = User(user.id, user.name, user.email)
            users_list.append(select_user)
        return users_list

    def get_user_by_id(self, search_id):
        model_user = self.session.query(
            UserModel).filter_by(id=search_id).first()
        search_user = User(model_user.id, model_user.name, model_user.email)
        return search_user


class SqlAlchemyExpenseRepository(IExpenseRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def save_expense(self, expense: Expense):
        db_expense = ExpenseModel(
            id=str(expense.id),
            expense_value=Decimal(expense.expense_value.value),
            description=str(expense.description),
            date=str(expense.date),
            category=str(expense.category),
            id_user=str(expense.id_user)
        )
        self.session.add(db_expense)
        self.session.commit()

    def filter_by_category(self, search_category):
        model_expense = self.session.query(
            ExpenseModel).filter_by(category=search_category).with_for_update().first()

        query_expense = Expense(model_expense.id, model_expense.expense_value, model_expense.description,
                                model_expense.date, model_expense.category, model_expense.id_user)
        return query_expense
