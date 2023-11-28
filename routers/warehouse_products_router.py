import inspect

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.warehouse_products_func import all_warehouses, create_warehouse_e, update_warehouse_e
from models.warehouse import Warehouses
from utils.auth import get_current_user
from utils.db_operations import get_in_db
from schemas.warehouse_products_schemas import Warehouse_products_create, Warehouse_products_update
from schemas.users_schemas import CreateUser
from db import database
from utils.role_checker import *

warehouses_router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses operation"]
)


@warehouses_router.get("/get_warehouses")
def get_warehouses(search: str = None, id: int = 0, page: int = 0, limit: int = 25, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_user)):
    role_admin(current_user) or role_driver(current_user) or role_operator(current_user) or role_warehouser(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Warehouses, id)
    return all_warehouses(search, page, limit, db)


@warehouses_router.post("/create_warehouse")
def create_warehouse(new_warehouse: Warehouse_products_create, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_admin(current_user) or role_driver(current_user) or role_operator(current_user) or role_warehouser(current_user)    
    create_warehouse_e(new_warehouse, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@warehouses_router.put("/update_warehouse")
def update_warehouse(this_warehouse: Warehouse_products_update, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_admin(current_user) or role_driver(current_user) or role_operator(current_user) or role_warehouser(current_user)    
    update_warehouse_e(this_warehouse, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






