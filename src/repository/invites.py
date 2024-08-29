from fastapi import HTTPException, status
from src.model.group import Group
from src.model.group_members import Role
from src.model.invites import Invites, Statuses
from src.repository.group import get_group_by_id, get_group_name_by_id
from src.repository.group_member import create_group_member, is_admin_user
from src.schema.invites import CreateInviteSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

def create_invite(payload: CreateInviteSchema, user_id: str, session: Session):
    if(is_admin_user(session=session,user_id=user_id, group_id=payload.group_id)):
        db_invite = Invites(**payload.dict())
        db_invite.invited_by = user_id
        db_invite.group_name = get_group_name_by_id(session=session, id=payload.group_id)
        db_invite.status = Statuses.pending
        session.add(db_invite)
        session.commit()
        session.refresh(db_invite)
        return db_invite
    else:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Not authorized to send request")

def reject_invite(id: int, user_id: str, session: Session):
    invite: Invites = session.query(Invites).filter(Invites.id == id).filter(Invites.invitee == user_id).one_or_none()
    if invite is None:
        return None
    else:
        invite.status = Statuses.reject
        session.add(invite)
        session.commit()
        session.refresh(invite)
        return invite

def all_my_invites(user_id: str, session: Session):
    return session.query(Invites).filter(Invites.invitee == user_id).filter(Invites.status == Statuses.pending)

def accept_invite(id: int, user_id: str, session: Session):
    try:
        with session.begin():
            invite: Invites = session.query(Invites).filter(Invites.id == id).filter(Invites.invitee == user_id).one_or_none()
            if invite is None:
                return None
            invite.status = Statuses.accept
            # group: Group = get_group_by_id(id=invite.invited_by, session=session)
            create_group_member(group_id= invite.group_id, user_id=user_id, role = Role.member, session=session)
            session.add(invite)
            session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.with_traceback)