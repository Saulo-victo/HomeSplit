import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
load_dotenv()

SQL_ALCHEMY_DATABASE_URL = os.getenv('SQL_ALCHEMY_DATABASE_URL')

engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={
                       'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
