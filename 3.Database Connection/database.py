from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL="sqlite:///./todos.db"

# SQLALCHEMY_DATABASE_URL="postgresql://postgres:1234@localhost/database_name"  # for local postgres database


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:1234@localhost:5432/postgres" # for local postgres database

# engine=create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False}) # For SQL database

engine=create_engine(SQLALCHEMY_DATABASE_URL) # For post gray sql

sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()


