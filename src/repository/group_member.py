from sqlalchemy import select
from src.model.group_members import GroupMember, Role
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.model.user import User

# from src.repository.group import get_groups_by_ids


def create_group_member(group_id: int, user_id:int, role: Role, session: Session):
    db_gm = GroupMember(group_id=group_id, 
                        user_id=user_id, 
                        role= role if role is not None else Role.admin, 
                        is_active= True)
    session.add(db_gm)
    return db_gm

def get_user_groups(session:Session, user_id: int):
    db_gms: list[GroupMember] = session.query(GroupMember).filter(
                                GroupMember.user_id == user_id).filter(
                                GroupMember.is_active == True)
    id = list(map(lambda gms: gms.group_id, db_gms))
    return id

def validate_user_group(session: Session, user_id: int, group_id: int):
    if session.query(GroupMember).filter(GroupMember.user_id == user_id).filter(GroupMember.group_id == group_id).filter(GroupMember.is_active == True).count() > 0:
        return True
    else:
        return False
    
def is_admin_user(session: Session, user_id: int, group_id: int):
    if session.query(GroupMember).filter(GroupMember.user_id == user_id).filter(GroupMember.group_id == group_id).filter(GroupMember.role == Role.admin).filter(GroupMember.is_active == True).count() > 0:
        return True
    else:
        return False
    
def get_users_in_group(session: Session, group_id: int, user_id: int):
    if validate_user_group(session=session, user_id=user_id, group_id=group_id):
        query = ( select(User.email, User.name.label('name'), GroupMember.role)
            .join(GroupMember, User.id == GroupMember.user_id)
            .filter(GroupMember.group_id == group_id).filter(GroupMember.is_active == True)
            .filter(User.is_active == True)
        )
        result = session.execute(query)
        users = result.mappings().all()
        
        return users
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid group id fro user")