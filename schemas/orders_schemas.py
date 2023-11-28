import datetime

from pydantic import BaseModel


class CreateOrder(BaseModel):
    name: str
    operator_id: int
    driver_id: int
    warehouser_id: int
    orienter: str
    customer_loc_id: int
    branch_id: int
 

class UpdateOrder(BaseModel):
    id: int
    name: str
    status: str
    operator_id: int
    driver_id: int
    warehouser_id: int
    orienter: str
    customer_loc_id: int
    branch_id: int

