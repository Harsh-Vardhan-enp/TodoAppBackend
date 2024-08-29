
from pydantic import BaseModel

from src.model.invites import Statuses


class InviteSchemaBase(BaseModel):
    # id: int
    pass
    
    
class CreateInviteSchema(InviteSchemaBase):
    group_id:int
    # group_name: str
    invitee: int

class UpdateInviteSchema(InviteSchemaBase):
    id: int
    # pass

class InviteSchema(CreateInviteSchema):
    id: int
    status: Statuses
    group_name: str
    invited_by: int
    class Config:
        orm_mode = True
    