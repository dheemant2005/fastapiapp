from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/student_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLoanLocal = sessionmaker(automatic=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   
