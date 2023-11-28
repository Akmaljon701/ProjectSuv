from pydantic import BaseModel

class CreateUserProduct(BaseModel):
    name: str
    product_id: int
    quantity: int
    branch_id: int

class UpdateUserProduct(BaseModel):
    id: int
    name: str
    product_id: int
    quantity: int
    branch_id: int