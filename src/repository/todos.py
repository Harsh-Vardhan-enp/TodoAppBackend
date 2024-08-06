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

def get_my_todos(session:Session, assigned_to: int):
    return session.query(Todos).filter(Todos.assigned_to == assigned_to)

def get_created_todos(session:Session, created_by: int):
    return session.query(Todos).filter(Todos.created_by == created_by)

def complete_todo(session: Session, id: int, assigned_to: int):
    todo: Todos = session.query(Todos).filter(id = id)
    if todo.assigned_to == assigned_to :
        db_todo = todo.dict()
        db_todo.is_completed = True
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
    else:
        pass