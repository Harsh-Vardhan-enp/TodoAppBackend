from sqlalchemy import Column, DateTime, ForeignKey, Integer, PrimaryKeyConstraint, String, func
from src.db import Base
from sqlalchemy.orm import relationship

class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable= False)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    
    
    PrimaryKeyConstraint("id", name="pk_group_id")
    creator = relationship('User', foreign_keys=[created_by])
    members = relationship('GroupMember', back_populates='group')
    