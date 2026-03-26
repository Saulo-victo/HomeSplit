from fastapi import FastAPI, Request
from src.infrastructure.database import Base, engine
from src.api.routers import user_route, expense_router
from src.domain.exceptions import InvalidEmail, InvalidCreateUser, InvalidValue, UserNotFound, ExpenseNotFound
from fastapi.responses import JSONResponse
from http import HTTPStatus


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_route.router)
app.include_router(expense_router.router)


@app.exception_handler(InvalidCreateUser)
def user_exception_handler(request: Request, exc):
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': str(exc)})


@app.exception_handler(InvalidEmail)
def email_exception_handler(request: Request, exc):
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': str(exc)})


@app.exception_handler(InvalidValue)
def invalid_value_excpetion_handler(request: Request, exc):
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': str(exc)})


@app.exception_handler(UserNotFound)
def invalid_value_excpetion_handler(request: Request, exc):
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': str(exc)})


@app.exception_handler(ExpenseNotFound)
def expense_not_found_expcetion_handler(request: Request, exc):
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': str(exc)})
