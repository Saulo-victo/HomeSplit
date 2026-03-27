from src.domain.entities import User, Expense, ExpenseWithUserName
from sqlalchemy.orm import Session, joinedload
from src.domain.interfaces import IExpenseRepository, IUserRepository
from decimal import Decimal
from src.infrastructure.models import UserModel, ExpenseModel
from src.domain.exceptions import ExpenseNotFound
from datetime import datetime, date
from sqlalchemy import extract


class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def save_user(self, user: User) -> None:
        db_user = UserModel(
            id=str(user.id),
            name=str(user.name),
            email=str(user.email.value),
            password=str(user.password)
        )
        self.session.add(db_user)
        self.session.commit()

    def get_all_users(self):
        users_list = []
        model_users = self.session.query(UserModel).all()
        for user in model_users:
            select_user = User(user.id, user.name, user.email, user.password)
            users_list.append(select_user)
        return users_list

    def get_user_by_id(self, search_id):
        model_user = self.session.query(
            UserModel).filter_by(id=search_id).first()
        if not model_user:
            return None
        search_user = User(model_user.id, model_user.name,
                           model_user.email, model_user.password)
        return search_user

    def get_user_by_email(self, email_search):
        model_user = self.session.query(
            UserModel).filter_by(email=email_search).first()
        if not model_user:
            return None
        search_user = User(model_user.id, model_user.name,
                           model_user.email, model_user.password)
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
            ExpenseModel).filter_by(category=search_category).options(joinedload(ExpenseModel.user)).all()
        expenses = [ExpenseWithUserName(expense.id, expense.expense_value, expense.description,
                                        expense.date, expense.category, expense.id_user, expense.user.name)for expense in model_expense]
        return expenses

    def get_all_expenses(self):
        model_expense = self.session.query(
            ExpenseModel).options(joinedload(ExpenseModel.user)).all()
        expenses = [ExpenseWithUserName(expense.id, expense.expense_value, expense.description,
                                        expense.date, expense.category, expense.id_user, expense.user.name)for expense in model_expense]
        return expenses

    def delete_expense(self, id_expense):
        model_expense = self.session.query(
            ExpenseModel).filter_by(id=id_expense).delete()
        if not model_expense:
            raise ExpenseNotFound('Despesa não encontrada')
        self.session.commit()

    def filter_by_month(self, search_month):
        current_year = date.today().year
        model_expense = self.session.query(ExpenseModel).filter(
            extract('month', ExpenseModel.date) == search_month, extract('year', ExpenseModel.date) == current_year).all()

        expenses = [ExpenseWithUserName(expense.id, expense.expense_value, expense.description,
                                        expense.date, expense.category, expense.id_user, expense.user.name)for expense in model_expense]

        return expenses
