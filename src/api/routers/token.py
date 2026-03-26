from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.application.use_cases.get_user import GetUser
from src.infrastructure.security import verify_password, create_acess_token
from src.domain.exceptions import UnauthorizedLogin
from src.api.schemas import Token


memory_unit_of_work = SqlAlchemyUnitOfWork()


def get_user_use_case():
    register = GetUser(memory_unit_of_work)
    return register


router = APIRouter()


@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), use_case=Depends(get_user_use_case)):
    user = use_case.execute_get_user_by_email(form_data.username)
    if not user:
        raise UnauthorizedLogin('Email ou senha incorretos')

    if not verify_password(form_data.password, user.password):
        raise UnauthorizedLogin('Email ou senha incorretos')

    access_token = create_acess_token(data={'sub': user.email})

    return {"access_token": access_token, "token_type": "Bearer"}
