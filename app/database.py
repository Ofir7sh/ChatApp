from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import DATABASE_URL


# יצירת מנוע חיבור למסד הנתונים
engine = create_engine(DATABASE_URL)

# יצירת session factory – בסיס לכל פעולת קריאה/כתיבה
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# בסיס למודלים שלנו
Base = declarative_base()

# פונקציה שמנוהלת ע״י FastAPI כדי לפתוח ולסגור session לכל בקשה
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
