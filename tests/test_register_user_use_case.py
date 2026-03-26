# ---------- Importação das dependências ----------
import pytest
from src.application.use_cases.register_user import RegisterUser
from src.domain.entities import User
from src.domain.value_objects import Email
from src.application.use_cases.register_expense import AddExpense
from src.domain.interfaces import IUnitOfWork, IUserRepository, IExpenseRepository

# ---------- Definição das classes fakes ----------


class FakeUserRepository(IUserRepository):
    def __init__(self):
        self.users = [User(id='58919f6e-6732-4790-a060-6cb815af5672',
                           name='Saulo', email=Email(value='saulovicto01@gmail.com'))]

    def save_user(self, user) -> None:
        self.users.append(user)

    def get_all_users(self):
        return self.users

    def get_user_by_id(self, search_id):
        for user in self.users:
            if user.id == search_id:
                return user


class FakeExpenseRepository(IExpenseRepository):
    def __init__(self):
        self.expenses = []

    def save_expense(self, expense) -> None:
        self.expenses.append(expense)

    def filter_by_category(self):
        pass

    def get_all_expenses(self):
        return self.expenses


class UnitOfWorkFake(IUnitOfWork):
    def __init__(self):
        self.user = FakeUserRepository()
        self.expenses = FakeExpenseRepository()

    def commit(self, user, expense) -> None:
        self.user.save_user(user)
        self.expenses.save_expense(expense)

    def rolback(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

# ---------- Configuração dos testes ----------


@pytest.fixture
def uow_fake():
    return UnitOfWorkFake()


def test_deve_registrar_usuario_com_sucesso(uow_fake):
    register = RegisterUser(uow_fake)

    new_user = register.execute("Lia", "lia123@gmail.com")

    users = uow_fake.user.get_all_users()
    assert len(users) == 2
    assert new_user.name == "Lia"
    assert new_user.email.value == "lia123@gmail.com"


def test_deve_adicionar_despesa_para_usuario_existente(uow_fake):
    register_expense = AddExpense(uow_fake)
    user_id_existente = "58919f6e-6732-4790-a060-6cb815af5672"

    register_expense.execute(
        525.31, "Teste de despesa", "Casa", user_id_existente
    )

    expenses = uow_fake.expenses.get_all_expenses()
    assert len(expenses) == 1
    assert expenses[0].description == "Teste de despesa"
    assert expenses[0].expense_value.value == 525.31
