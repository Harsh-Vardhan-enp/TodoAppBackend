
from fastapi import HTTPException, status
from src.model.group import Group
from src.model.group_members import GroupMember, Role
from src.repository.group_member import create_group_member
from src.schema.group import CreateGroupSchema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def create_groups(session:Session, group: CreateGroupSchema, created_by: int):
    
    # session.add(db_group)
    # checkpoint_b = session.begin_nested()
    try:
        with session.begin():
            db_group = Group(**group.dict(), created_by = created_by)
            session.add(db_group)
            session.flush()
            db_gm = GroupMember(group_id=db_group.id, 
                        user_id=created_by, 
                        role= Role.admin, 
                        is_active= True)
            session.add(db_gm)
            session.refresh(db_group)
            return db_group
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.with_traceback)
        
            
    # try:
    #     session.commit()
    #     session.refresh(db_group)
    #     create_group_member(group_id=db_group.id, user_id= created_by, role= Role.admin, session= session)
    #     session.commit()
    # except SQLAlchemyError as e:
    #     # checkpoint_b.rollback()
    #     session.rollback()
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.with_traceback)
    

def get_groups_by_ids(session: Session, ids: list[int]):
    return session.query(Group).filter(Group.id.in_(ids)).all()

def get_group_by_id(session: Session, id: int):
    return session.query(Group).filter(Group.id == id)

def get_group_name_by_id(session: Session, id: int):
    group =  session.query(Group).filter(Group.id == id).one_or_none()
    if group is not None:
        return group.name
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid group id")