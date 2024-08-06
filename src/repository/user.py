from src.model.user import User
from src.schema.user import CreateUserSchema
from sqlalchemy.orm import Session

def create_user(session:Session, user: CreateUserSchema):
    db_user = User(**user.dict())
    db_user.is_active = True
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user(session: Session, email: str):
    return session.query(User).filter(User.email == email).one()

def get_user_by_id(session: Session, id: int):
    return session.query(User).filter(User.id == id).one()