from pydantic import BaseModel, Field

from src.model.group_members import Role


class GMBaseSchema(BaseModel):
    group_id: int
    user_id: int
    
class CreateGMSchema(GMBaseSchema):
    role: Role 
    is_active: bool = Field(default=True)
    
class GMSchema(GMBaseSchema):
    role: Role
    is_active: bool = Field(default=True)
    class Config:
        orm_mode = True
    
class GMUserDetails(BaseModel):
    email: str
    name: str
    role: Role