from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from db import database
from schemas.users_schemas import CreateUser
from utils.auth import get_current_user
from utils.db_operations import get_in_db
from utils.role_checker import *
from functions.supplier_func import all_suppliers_r,create_supplier_r,update_supplier_r
from schemas.supplies_schemas import CreateSupplier,UpdateSupplier
from models.supplies import Supplies

suppliers_router = APIRouter(
    prefix="/supplies",
    tags=["Supplies Operations"]
)

@suppliers_router.get("/get_suppliers")
def all_suppliers(search: str = None, limit: int = 25, page: int = 0,db: Session = Depends(database),
                  current_user:CreateUser = Depends(get_current_user),id: int = 0):
    role_admin(current_user) or role_driver(current_user) or role_operator(current_user) or role_warehouser(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Supplies, id)
    return all_suppliers_r(search,limit,page,db)
@suppliers_router.post("/create_supplier")
def create_suppliers(new_supplier: CreateSupplier,db: Session = Depends(database),current_user: CreateUser = Depends(get_current_user)):
    role_admin(current_user) or role_driver(current_user) or role_operator(current_user) or role_warehouser(current_user)
    create_supplier_r(new_supplier,db,current_user)
    
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

@suppliers_router.put("/update_supplier")
def update_suppplier(this_supplier: UpdateSupplier,db: Session = Depends(database),current_user: CreateUser = Depends(get_current_user)):
    role_admin(current_user) or role_driver(current_user) or role_operator(current_user) or role_warehouser(current_user)
    update_supplier_r(this_supplier,db,current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")