from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from db import database
from functions.trades_func import all_trades_r, create_trade_r
from models.trades import Trades
from schemas.trades_schemas import CreateTrade
from schemas.users_schemas import CreateUser
from utils.auth import get_current_user
from utils.db_operations import get_in_db
from utils.role_checker import *

trades_router = APIRouter(
    prefix="/trades",
    tags=["Trades Operations"]
)

@trades_router.get("/get_trades")
def all_trades(search: str = None, limit: int = 25, page: int = 0,db: Session = Depends(database),
                  current_user:CreateUser = Depends(get_current_user),id: int = 0):
    role_admin(current_user) or role_driver(current_user) or role_operator(current_user) or role_warehouser(current_user)
    if page < 0 or limit < 0:
        raise HTTPException(status_code=400, detail="page yoki limit 0 dan kichik kiritilmasligi kerak")
    if id > 0:
        return get_in_db(db, Trades, id)
    all_trades_r(search,page,limit,db)
    
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
@trades_router.post("/create_trade")
def create_trades(new_trade: CreateTrade,db: Session = Depends(database),current_user: CreateUser = Depends(get_current_user)):
    role_admin(current_user) or role_driver(current_user) or role_operator(current_user) or role_warehouser(current_user)
    create_trade_r(new_trade,db,current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")

