from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import src.settings

print(src.settings.DATABASE_URL)
engine = create_engine(src.settings.DATABASE_URL,
                       pool_pre_ping=True,
                       pool_size=100,
                       max_overflow=300,
                       pool_timeout=60, 
                       echo=True, 
                       future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()