from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DATABASE_URL = "mssql+pymssql://sa:Os1234567!!@localhost:1433/ChatAppDB"

# יצירת מנוע חיבור למסד הנתונים
engine = create_engine(DATABASE_URL)

# יצירת session factory – בסיס לכל פעולת קריאה/כתיבה
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# בסיס למודלים שלנו
Base = declarative_base()

# פונקציה שמנוהלת ע״י FastAPI כדי לפתוח ולסגור session לכל בקשה
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
