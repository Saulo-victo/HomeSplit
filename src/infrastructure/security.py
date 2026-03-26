from pwdlib import PasswordHash
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode, decode, DecodeError
from fastapi.security import OAuth2PasswordBearer
from src.api.dependecies import get_uow
from src.domain.interfaces import IUnitOfWork
from fastapi import Depends
from src.domain.exceptions import UnauthorizedLogin

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACESS_TOKEN_EXPIRE_MINUTES')

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_acess_token(data: dict):
    to_econde = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + \
        timedelta(minutes=int(ACESS_TOKEN_EXPIRE_MINUTES))

    to_econde.update({'exp': expire})

    encoded_jwt = encode(to_econde, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), uow: IUnitOfWork = Depends(get_uow)):
    print(f"DEBUG: Token recebido: {token}")
    try:
        payload = decode(token, SECRET_KEY, algorithms=ALGORITHM)
        subject_email = payload.get('sub')
        print(subject_email)
        if not subject_email:
            raise UnauthorizedLogin('Usuário não autorizado')

    except DecodeError:
        raise UnauthorizedLogin('Usuário não autorizado')

    with uow:
        current_user = uow.user.get_user_by_email(subject_email)
        if not current_user:
            raise UnauthorizedLogin('Usuário não autorizado')
    return current_user
