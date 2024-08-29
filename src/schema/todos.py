from pydantic import BaseModel, EmailStr, Field


class TodosBaseSchema(BaseModel):
    agenda: str
    description: str
    group_id: int


class CreateTodosSchema(TodosBaseSchema):
    assigned_to: int

class CompleteTodoSchema(BaseModel):
    id:int

class Todoschema(TodosBaseSchema):
    id: int
    is_completed: bool= Field(default=False)
    created_by: int
    assigned_to: int

    class Config:
        orm_mode = True