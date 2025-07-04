from sqlalchemy import create_engine, text
from app.database import Base
from app.models import user, chat_room, message  # ודאי שכל המודלים מיובאים כאן
##TODO - Generic params

MASTER_DATABASE_URL = "mssql+pymssql://sa:Os1234567!!@localhost:1433/master"
APP_DB_NAME = "ChatAppDB"
APP_DATABASE_URL = f"mssql+pymssql://sa:Os1234567!!@localhost:1433/{APP_DB_NAME}"

def create_database():
    engine = create_engine(MASTER_DATABASE_URL, echo=True)

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
    Base.metadata.drop_all(bind=engine)  # ניתן למחוק אם לא רוצים למחוק טבלאות קיימות
    print("Dropped all tables.")
    Base.metadata.create_all(bind=engine)
    print("Created all tables.")

if __name__ == "__main__":
    create_database()
    create_tables()
