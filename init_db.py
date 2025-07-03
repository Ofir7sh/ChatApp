from sqlalchemy import create_engine, text
from app.database import Base
from app.database import DATABASE_URL
# master - default mmsql db
engine = create_engine("mssql+pymssql://sa:Os1234567!!@localhost:1433/master", isolation_level="AUTOCOMMIT")

def create_database():
    with engine.connect() as conn:
        print("Connected to master DB.")
        result = conn.execute(text("SELECT name FROM sys.databases WHERE name = 'ChatAppDB'"))
        if not result.fetchone():
            print("Creating ChatAppDB...")
            conn.execute(text("CREATE DATABASE ChatAppDB"))
            print("ChatAppDB created.")
        else:
            print("ChatAppDB already exists.")

def create_tables():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("All tables created.")

if __name__ == "__main__":
    create_database()
    create_tables()