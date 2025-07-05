from sqlalchemy import create_engine, text
from app.database import Base
from app.core.config import MASTER_DATABASE_URL, DATABASE_URL as APP_DATABASE_URL, DB_NAME as APP_DB_NAME
from app.models import user, chat_room, message  

def create_database():
    engine = create_engine(MASTER_DATABASE_URL, echo=True, isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT name FROM sys.databases WHERE name = '{APP_DB_NAME}'"))
        exists = result.fetchone()
        if not exists:
            conn.execute(text(f"CREATE DATABASE {APP_DB_NAME}"))
            print(f"Database {APP_DB_NAME} created.")
        else:
            print(f"Database {APP_DB_NAME} already exists.")

def create_tables():
    engine = create_engine(APP_DATABASE_URL, echo=True)
    # Base.metadata.drop_all(bind=engine) 
    # print("Dropped all tables.")
    Base.metadata.create_all(bind=engine, checkfirst=True)
    print("Created all tables.")

if __name__ == "__main__":
    create_database()
    create_tables()
