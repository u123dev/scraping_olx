import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


dotenv.load_dotenv()

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from .env
    Returns sqlalchemy engine instance
    """
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")  # "localhost"
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")

    engine = create_engine(f"postgresql://{user}:{password}@localhost/{database}")
    return engine

def create_table(engine):
    Base.metadata.create_all(engine)
