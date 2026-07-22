from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

engine = create_engine("sqlite:///myfile.db", isolation_level="AUTOCOMMIT")


def get_db():
    with Session(bind=engine) as session:
        return session
