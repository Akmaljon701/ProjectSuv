from datetime import date
from typing import List
from pydantic import BaseModel, validator
from sqlalchemy import *

from schemas.phones_schemas import CreatePhone, UpdatePhone

class CreateSupplier(BaseModel):
    name: str
    product_id: int
    quantity: int
    price: int
    date: date
    branch_id: int
    phones: List[CreatePhone]
    
    class Config:
        arbitrary_types_allowed = True

    @validator('date', pre=True)
    def parse_date(cls, value):
            if isinstance(value, str):
                return date.fromisoformat(value)
            return value


class UpdateSupplier(BaseModel):
    id: int
    name: str
    product_id: int
    quantity: int
    price: int
    date: date
    branch_id: int
    phones: List[UpdatePhone]
    class Config:
        arbitrary_types_allowed = True
    
    @validator('date', pre=True)
    def parse_date(cls, value):
            if isinstance(value, str):
                return date.fromisoformat(value)
            return value
