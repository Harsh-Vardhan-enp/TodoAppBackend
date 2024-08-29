from fastapi import HTTPException, status
from src.model.todos import Todos
from src.schema.todos import CreateTodosSchema
from sqlalchemy.orm import Session


def create_todos(session:Session, todos: CreateTodosSchema, created_by: str):
    db_todos = Todos(**todos.dict())
    db_todos.created_by = created_by
    session.add(db_todos)
    session.commit()
    session.refresh(db_todos)
    return db_todos

def get_my_todos(session:Session, assigned_to: int, group_id: int):
    return session.query(Todos).filter(Todos.assigned_to == assigned_to).filter(Todos.is_completed == False).filter(Todos.group_id == group_id)

def get_my_completed_todos(session:Session, assigned_to: int , group_id: int):
    return session.query(Todos).filter(Todos.assigned_to == assigned_to).filter(Todos.is_completed == True).filter(Todos.group_id == group_id)

def get_created_todos(session:Session, created_by: int, group_id: int):
    return session.query(Todos).filter(Todos.created_by == created_by).filter(Todos.is_completed == False).filter(Todos.group_id == group_id)

def delete_todo(session:Session, id: int, group_id: int):
    try:
        session.query(Todos).filter(Todos.group_id == group_id).filter(Todos.id == id).delete(synchronize_session=False)
        session.commit()
        return 1
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid deletion')

def complete_todo(session: Session, id: int, assigned_to: int, group_id: int): 
    try:
        todo: Todos = session.query(Todos).filter(Todos.group_id == group_id).filter(Todos.id == id ).one_or_none()
        todo
        if todo is None:
            return None
        if todo.assigned_to == assigned_to :
            todo.is_completed = True
            session.commit()
            return todo
    except :
        raise RuntimeError