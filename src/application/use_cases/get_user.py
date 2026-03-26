from src.domain.interfaces import IUnitOfWork


class GetUser:
    def __init__(self, repository: IUnitOfWork):
        self.uow = repository

    def execute_get_user_by_id(self, id_user):
        with self.uow as uow:
            expenses = self.uow.user.get_user_by_id(id_user)
            return expenses
