from src.domain.interfaces import IUnitOfWork


class GetExpenses:
    def __init__(self, repository: IUnitOfWork):
        self.uow = repository

    def execute_get_all_expenses(self):
        with self.uow as uow:
            expenses = self.uow.expense.get_all_expenses()
            return expenses

    def execute_get_expenses_by_category(self, search_category):
        with self.uow as uow:
            expenses = self.uow.expense.filter_by_category(search_category)
            return expenses

    def execute_delete_expense(self, id_expense):
        with self.uow as uow:
            expense = self.uow.expense.delete_expense(id_expense)
            return expense

    def execute_get_expenses_by_month(self, search_month):
        with self.uow as uow:
            expenses = self.uow.expense.filter_by_month(search_month)
            return expenses
