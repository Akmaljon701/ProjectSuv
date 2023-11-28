from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    comment: str
    branch_id: int
    user_id: int

class UpdateCategory(BaseModel):
    id: int
    name: str
    comment: str
    branch_id: int
    user_id: int
