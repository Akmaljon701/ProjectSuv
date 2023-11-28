from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.branch_func import all_branches, create_branche_r, update_branche_r
from models.branches import Branches
from utils.auth import get_current_user
from schemas.users_schemas import CreateUser
from utils.db_operations import get_in_db
from schemas.branch_schemas import CreateBranche,UpdateBranche
from db import database
from utils.role_checker import role_admin

branches_router = APIRouter(
    prefix="/branches",
    tags=["Branches operation"]
)


@branches_router.get("/get_branches")
def get_branches(search: str = None, id: int = 0, page: int = 0, limit: int = 25, status: bool = None, db: Session = Depends(database),
              current_user: CreateUser = Depends(get_current_user)):
    role_admin(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Branches, id)
    return all_branches(search, page, limit, status, db)



@branches_router.post("/create_branches")
def create_branches(new_branche: CreateBranche, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_admin(current_user)
    create_branche_r(new_branche, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@branches_router.put("/update_branches")
def update_branches(this_branche: UpdateBranche, db: Session = Depends(database),
                current_user: CreateUser = Depends(get_current_user)):
    role_admin(current_user)
    update_branche_r(this_branche, db, current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")






