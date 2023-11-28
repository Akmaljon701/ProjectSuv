from fastapi import HTTPException
from functions.incomes_func import create_income_r
from models.branches import Branches
from models.kassa import Kassas
from models.orders import Orders
from models.trades import Trades
from sqlalchemy.orm import joinedload
from models.users import Users
from models.warehouse import Warehouses
from utils.db_operations import get_in_db, save_in_db
from utils.paginatsiya import pagination


def all_trades_r(search, page, limit, db):
    # trades = db.query(Trades).join(Trades.warehouse_pr_id).join(Trades.order_id).join(Trades.user_id).options(joinedload(Trades.warehouse_pr_id), joinedload(Trades.order_id),joinedload(Trades.user_id))
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = db.query(Trades).filter(Trades.name.like(search_formatted))
    trades = db.query(Trades).filter(search_filter).order_by(Trades.name.asc())
    return pagination(trades, page, limit)


def create_trade_r(data, db, thisuser):
    if db.query(Trades).filter(Trades.order_id == data.order_id).first():
                raise HTTPException(status_code=400, detail="Bunday trade orderga allaqachon allaqachon bazada bor")
    order = get_in_db(db, Orders, data.order_id)
    if order.status  == "2" and get_in_db(db,Warehouses,data.warehouse_pr_id) != None and get_in_db(db,Branches,data.branch_id) != None:
        product = db.query(Warehouses).filter(Warehouses.id == data.warehouse_pr_id).first()
        new_product_quantity = product.quantity - data.quantity
        price = product.price * data.quantity
        if new_product_quantity >= 0:
            new_trade = Trades(
                name=data.name,
                warehouse_pr_id=data.warehouse_pr_id,
                price=price,
                quantity=data.quantity,#false,
                order_id=data.order_id,
                user_id=thisuser.id,
                branch_id=data.branch_id

            )
            save_in_db(db, new_trade)
            db.query(Warehouses).filter(Warehouses.id == data.warehouse_pr_id).update({
            Warehouses.quantity: new_product_quantity
        })
            db.commit()
            kassa = db.query(Kassas).filter(Kassas.branch_id == data.branch_id).first()
            create_income_r("trade",data.order_id,kassa.id,thisuser.id,"TRade Income","trade",price,data.branch_id,db)
        else:
             raise HTTPException(status_code=400,detail="Warehouse da buncha maxsulot mavjud emas")

