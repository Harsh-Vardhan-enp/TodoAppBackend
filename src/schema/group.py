
from pydantic import BaseModel


class GroupBaseSchema(BaseModel):
    name: str
    
class CreateGroupSchema(GroupBaseSchema):
    pass

class GroupSchema(GroupBaseSchema):
    id: int
    created_by: int
    class Config:
        orm_mode = True