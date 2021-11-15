from typing import ParamSpecArgs
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

password = os.getenv('PASSWORD')
server_name = os.getenv('SERVER_NAME')
database_name = os.getenv('DATABASE_NAME')

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:{}@{}/{}'.format(password, server_name, database_name)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        