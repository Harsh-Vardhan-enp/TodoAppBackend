from sqlalchemy import Column, Integer, String
from src.db import Base


class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, nullable=False, primary_key= True)
    log_type = Column(String(100), nullable=False)
    log_desc = Column(String(200), nullable=True)