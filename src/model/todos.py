from sqlalchemy import Boolean, Column, ForeignKey, Integer, PrimaryKeyConstraint, String, ForeignKeyConstraint
from src.db import Base
from sqlalchemy.orm import relationship

class Todos(Base):
    __tablename__ = 'todos'
    id = Column(Integer, nullable=False, primary_key= True)
    agenda = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)
    assigned_to = Column(Integer, ForeignKey('user.id'), nullable=False)
    is_completed = Column(Boolean, default=False)

    PrimaryKeyConstraint("id", name="pk_todo_id")
    creator = relationship('User', foreign_keys=[created_by])
    assignee = relationship('User', foreign_keys=[assigned_to])
    