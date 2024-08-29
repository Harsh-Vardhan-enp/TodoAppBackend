import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, PrimaryKeyConstraint, String, func
from src.db import Base
from sqlalchemy.orm import relationship

class Role(enum.Enum):
    admin='admin'
    member='member'

class GroupMember(Base):
    __tablename__ = "group_member"
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True, nullable=False)
    
    __table_args__ = (
        PrimaryKeyConstraint('group_id', 'user_id', name='pk_group_member'),
    )
    user = relationship('User', foreign_keys=[user_id])
    group = relationship('Group', foreign_keys=[group_id])
    