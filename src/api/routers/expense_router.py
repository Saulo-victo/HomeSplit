from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from fastapi import APIRouter
from src.application.use_cases.register_expense import AddExpense
from src.api.schemas import RequestExpenseRegister, ResponseExpenseRegister
from http import HTTPStatus
from fastapi import Depends

memory_unit_of_work = SqlAlchemyUnitOfWork()


def get_register_expense():
    register = AddExpense(memory_unit_of_work)
    return register


router = APIRouter(
    prefix='/expenses',
    tags=['expenses']
)


@router.post('/{id_user_register}', response_model=ResponseExpenseRegister, status_code=HTTPStatus.CREATED)
def register_expense(id_user_register: str, expense_data: RequestExpenseRegister, use_case=Depends(get_register_expense)):
    expense = use_case.execute(expense_data, id_user_register)
    return {
        'id': str(expense.id),
        'expense_value': str(expense.expense_value.value),
        'description': str(expense.description),
        'date': str(expense.date),
        'category': str(expense.category),
        'id_user': str(expense.id_user)
    }


@router.get('/', response_model=ResponseExpenseRegister, status_code=HTTPStatus.OK)
def get_all_register_expenses()
