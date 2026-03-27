from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from fastapi import APIRouter
from src.domain.entities import User
from src.application.use_cases.register_expense import AddExpense
from src.application.use_cases.get_expenses import GetExpenses
from src.api.schemas import RequestExpenseRegister, ResponseExpense, ResponseExpenseWithNameUser, ResponseExpenseSumary
from http import HTTPStatus
from fastapi import Depends
from datetime import datetime
from src.infrastructure.security import get_current_user

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


@router.post('/', response_model=ResponseExpense, status_code=HTTPStatus.CREATED)
def register_expense(expense_data: RequestExpenseRegister, use_case=Depends(use_case_register_expense), user: User = Depends(get_current_user)):
    expense = use_case.execute(expense_data, user.id)
    return {
        'id': str(expense.id),
        'expense_value': str(expense.expense_value.value),
        'description': str(expense.description),
        'date': str(expense.date),
        'category': str(expense.category),
        'id_user': str(expense.id_user)
    }


@router.get('/', response_model=list[ResponseExpenseWithNameUser], status_code=HTTPStatus.OK)
def get_all_register_expenses(use_case=Depends(use_case_get_expenses), current_user=Depends(get_current_user)):
    all_expenses = use_case.execute_get_all_expenses()
    return all_expenses


@router.get('/category/{category}', response_model=list[ResponseExpenseWithNameUser], status_code=HTTPStatus.OK)
def get_all_register_by_category(category: str, use_case=Depends(use_case_get_expenses), current_user=Depends(get_current_user)):
    expenses_by_category = use_case.execute_get_expenses_by_category(category)
    return expenses_by_category


@router.delete('/delete/', status_code=HTTPStatus.OK)
def delete_register_expense(id_expense: str, use_case=Depends(use_case_get_expenses), current_user=Depends(get_current_user)) -> None:
    use_case.execute_delete_expense(id_expense)
    return {'Despesa Excluida'}


@router.get('/month/{search_month}', response_model=list[ResponseExpense], status_code=HTTPStatus.OK)
def get_all_expenses_by_month(search_month: int, use_case=Depends(use_case_get_expenses), current_user=Depends(get_current_user)):
    expenses_by_month = use_case.execute_get_expenses_by_month(search_month)
    return expenses_by_month


@router.get('/sumary/', response_model=ResponseExpenseSumary, status_code=HTTPStatus.OK)
def get_sumary_expense_by_month(search_month: int, use_case=Depends(use_case_get_expenses), current_user=Depends(get_current_user)):
    list_expenses = use_case.execute_get_expenses_by_month(search_month)
    total_spend = 0
    total_mercado = 0
    total_internet = 0
    total_aluguel = 0
    total_pets = 0
    total_energia = 0
    total_agua = 0
    total_manutencao = 0
    total_outros = 0
    total_by_week = {
        "Semana 1": 0.0,
        "Semana 2": 0.0,
        "Semana 3": 0.0,
        "Semana 4": 0.0,
        "Semana 5": 0.0
    }
    for expense in list_expenses:
        total_spend = expense.expense_value + total_spend

        if expense.category == 'Mercado':
            total_mercado += expense.expense_value

        elif expense.category == 'Internet':
            total_internet += expense.expense_value

        elif expense.category == 'Aluguel':
            total_aluguel += expense.expense_value

        elif expense.category == 'Pets':
            total_pets += expense.expense_value

        elif expense.category == 'Energia':
            total_energia += expense.expense_value

        elif expense.category == 'Água':
            total_agua += expense.expense_value

        elif expense.category == 'Manutenção':
            total_manutencao += expense.expense_value

        elif expense.category == 'Outros':
            total_outros += expense.expense_value

        if isinstance(expense.date, str):
            dt_obj = datetime.fromisoformat(expense.date)
        else:
            dt_obj = expense.date
        dia = dt_obj.day
        num_semana = (dia - 1) // 7 + 1
        label = f"Semana {num_semana}"
        valor = float(expense.expense_value)
        total_by_week[label] += valor

    total_by_category = {
        "Mercado": total_mercado,
        "Internet": total_internet,
        "Aluguel": total_aluguel,
        "Pets": total_pets,
        "Energia": total_energia,
        "Água": total_agua,
        "Manutenção": total_manutencao,
        "Outros": total_outros
    }

    top_category = max(total_by_category, key=total_by_category.get)
    top_value_category = total_by_category[top_category]

    return {
        "total_spend": total_spend,
        "top_category": top_category,
        "top_value_category": top_value_category,
        "total_by_category": total_by_category,
        "total_by_week": total_by_week,
        "list_expenses": list_expenses
    }
