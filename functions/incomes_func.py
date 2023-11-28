from datetime import datetime
from functions.kassa_func import update_kassa_r

from models.incomes import Incomes
from models.kassa import Kassas
from utils.db_operations import get_in_db, save_in_db
from utils.paginatsiya import pagination


def all_income_r(search, page, limit, db):
    if search :
        search_formatted = "%{}%".format(search)
        search_filter = (Incomes.name.like(search_formatted))
    else :
        search_filter = Incomes.id > 0
    income = db.query(Incomes).filter(search_filter).order_by(Incomes.name.asc())
    return pagination(income, page, limit)


def create_income_r(source,source_id,kassa_id,user_id,comment,type,money,branch_id,db):
    kassa = get_in_db(db,Kassas,kassa_id)
    if kassa:
        new_income = Incomes(
            name="from trade",
            money=money,
            date=datetime.today(),
            comment=comment,
            kassa_id=kassa_id,
            user_id=user_id,
            branch_id=branch_id,
            type=type,
            source=source,
            source_id=source_id
        )
        save_in_db(db, new_income)
        update_kassa_r(kassa_id,money,db,user_id)
