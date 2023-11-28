from typing import List
from pydantic import BaseModel

from schemas.phones_schemas import CreatePhone, UpdatePhone


class Warehouse_products_create(BaseModel):
    name: str
    product_id: int
    quantity: int
    price: int
    branch_id: int
    phones: List[CreatePhone]

class Warehouse_products_update(BaseModel):
    id: int
    name: str
    product_id: int
    quantity: int
    price: int
    branch_id: int
    phones: List[UpdatePhone]