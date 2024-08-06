from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    email:EmailStr
    

class CreateUserSchema(UserBaseSchema):
    hashed_pass:str = Field(alias='password')
    name: str

class UserSchema(UserBaseSchema):
    id: int
    name: str
    is_active: bool= Field(default=False)

    class Config:
        orm_mode = True

class UserLoginSchema(UserBaseSchema):
    email: EmailStr = Field(alias="username")
    password: str