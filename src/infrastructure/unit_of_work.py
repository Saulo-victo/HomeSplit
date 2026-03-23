from src.infrastructure.database import SessionLocal
from src.infrastructure.repositories import SqlAlchemyExpenseRepository, SqlAlchemyUserRepository


class SqlAlchemyUnitOfWork:
    def __enter__(self):
        self.session = SessionLocal()
        self.user = SqlAlchemyUserRepository(self.session)
        self.expense = SqlAlchemyExpenseRepository(self.session)
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()
