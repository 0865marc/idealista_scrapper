import os

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/db"
)

# Crear el engine con algunas configuraciones útiles
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True para ver las consultas SQL
    pool_pre_ping=True,  # Verificar conexión antes de usar
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
