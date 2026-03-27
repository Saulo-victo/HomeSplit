from src.infrastructure.database import Base
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import ForeignKey, String, Numeric, Date
from datetime import date


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    expense = relationship('ExpenseModel', back_populates='user')


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    expense_value: Mapped[str] = mapped_column(
        Numeric(precision=10, scale=2), nullable=False)
    description: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String, nullable=False)
    id_user: Mapped[str] = mapped_column(String, ForeignKey('users.id'))
    user = relationship('UserModel', back_populates="expense")
