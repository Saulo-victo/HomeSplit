from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from src.domain.entities import User
from src.domain.value_objects import Email
from src.domain.exceptions import InvalidEmail
import uuid


class RegisterUser:
    def __init__(self, repository: SqlAlchemyUnitOfWork):
        self.uow = repository

    def execute(self, name, email):
        with self.uow as uow:
            id = str(uuid.uuid4())
            name = str(name)
            users = self.uow.user.get_all_users()
            for user in users:
                if email == user.email:
                    raise InvalidEmail("Email já cadastrado")
            email = Email(email)

            user = User(id, name, email)

            uow.user.save_user(user)
            return user
