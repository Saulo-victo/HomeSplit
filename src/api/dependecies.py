from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


def get_uow():
    uow = SqlAlchemyUnitOfWork()
    try:
        yield uow
    finally:
        pass
