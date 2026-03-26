from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from fastapi import APIRouter
from src.application.use_cases.register_user import RegisterUser
from src.api.schemas import RequestUserRegister, ResponseUserRegister
from http import HTTPStatus
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from src.domain.exceptions import InvalidCreateUser



memory_unit_of_work = SqlAlchemyUnitOfWork()


def get_register_use_case():
    register = RegisterUser(memory_unit_of_work)
    return register


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/', response_model=ResponseUserRegister, status_code=HTTPStatus.CREATED)
def register_user(request: RequestUserRegister, use_case=Depends(get_register_use_case)):
    try:
        user = use_case.execute(**request.model_dump())
        return {
            'id': str(user.id),
            'name': str(user.name),
            'email': str(user.email)
        }
    except IntegrityError:
        raise InvalidCreateUser('Usuário já cadastrado')
