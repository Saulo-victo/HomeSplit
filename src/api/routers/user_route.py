from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from fastapi import APIRouter
from src.application.use_cases.register_user import RegisterUser
from src.application.use_cases.get_user import GetUser
from src.api.schemas import RequestUserRegister, ResponseUser
from http import HTTPStatus
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from src.domain.exceptions import InvalidCreateUser, UserNotFound


memory_unit_of_work = SqlAlchemyUnitOfWork()


def get_register_user_use_case():
    register = RegisterUser(memory_unit_of_work)
    return register


def get_user_use_case():
    register = GetUser(memory_unit_of_work)
    return register


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/', response_model=ResponseUser, status_code=HTTPStatus.CREATED)
def register_user(request: RequestUserRegister, use_case=Depends(get_register_user_use_case)):
    try:
        user = use_case.execute(**request.model_dump())
        return {
            'id': str(user.id),
            'name': str(user.name),
            'email': str(user.email)
        }
    except IntegrityError:
        raise InvalidCreateUser('Usuário já cadastrado')


@router.get('/{user_id}', response_model=ResponseUser, status_code=HTTPStatus.OK)
def get_user_by_id(user_id, use_case=Depends(get_user_use_case)):
    try:
        user = use_case.execute_get_user_by_id(user_id)
        return user
    except:
        raise UserNotFound('Usuário não encontrado')
