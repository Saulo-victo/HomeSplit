from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from fastapi import APIRouter
from src.application.use_cases.register_expense import AddExpense
from src.application.use_cases.get_expenses import GetExpenses
from src.api.schemas import RequestExpenseRegister, ResponseExpense, ResponseExpenseWithNameUser
from http import HTTPStatus
from fastapi import Depends

memory_unit_of_work = SqlAlchemyUnitOfWork()


def use_case_register_expense():
    register = AddExpense(memory_unit_of_work)
    return register


def use_case_get_expenses():
    all_expenses = GetExpenses(memory_unit_of_work)
    return all_expenses


router = APIRouter(
    prefix='/expenses',
    tags=['expenses']
)


@router.post('/{id_user_register}', response_model=ResponseExpense, status_code=HTTPStatus.CREATED)
def register_expense(id_user_register: str, expense_data: RequestExpenseRegister, use_case=Depends(use_case_register_expense)):
    expense = use_case.execute(expense_data, id_user_register)
    return {
        'id': str(expense.id),
        'expense_value': str(expense.expense_value.value),
        'description': str(expense.description),
        'date': str(expense.date),
        'category': str(expense.category),
        'id_user': str(expense.id_user)
    }


@router.get('/', response_model=list[ResponseExpenseWithNameUser], status_code=HTTPStatus.OK)
def get_all_register_expenses(use_case=Depends(use_case_get_expenses)):
    all_expenses = use_case.execute_get_all_expenses()
    return all_expenses


@router.get('/{category}', response_model=list[ResponseExpenseWithNameUser], status_code=HTTPStatus.OK)
def get_all_register_by_category(category: str, use_case=Depends(use_case_get_expenses)):
    expenses_by_category = use_case.execute_get_expenses_by_category(category)
    return expenses_by_category


@router.delete('/{id_expense}', status_code=HTTPStatus.OK)
def delete_register_expense(id_expense: str, use_case=Depends(use_case_get_expenses)) -> None:
    use_case.execute_delete_expense(id_expense)
    return {'Despesa Excluida'}
