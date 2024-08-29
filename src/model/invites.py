import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, PrimaryKeyConstraint, String, func
from src.db import Base
from sqlalchemy.orm import relationship

class Statuses(enum.Enum):
    accept='accept'
    reject='reject'
    pending= 'pending'

class Invites(Base):
    __tablename__ = "invites"
    id = Column(Integer, primary_key=True, autoincrement=True)
    invitee = Column(Integer, ForeignKey('user.id'), nullable=False)
    invited_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)
    group_name = Column(String(100), nullable= False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(Statuses), nullable=False)
    
    PrimaryKeyConstraint("id", name="pk_invite_id")
    invitee_fk = relationship('User', foreign_keys=[invitee])
    invited_by_fk = relationship('User', foreign_keys=[invited_by])
    group_id_fk = relationship('Group', foreign_keys=[group_id])