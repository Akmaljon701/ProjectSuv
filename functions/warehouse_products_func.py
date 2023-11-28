from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from functions.phones_func import create_phone, update_phone
from models.phones import Phones
from utils.db_operations import save_in_db, get_in_db
from utils.paginatsiya import pagination
from models.warehouse import Warehouses


def all_warehouses(search, page, limit, db):
    warehouses = db.query(Warehouses).join(Warehouses.phones).options(joinedload(Warehouses.phones))
    if search:
        search_formatted = "%{}%".format(search)
        warehouses = warehouses.filter(Warehouses.name.like(search_formatted))
    warehouses = warehouses.order_by(Warehouses.name.asc())
    return pagination(warehouses, page, limit)


def create_warehouse_e(form, db, thisuser):
    if db.query(Warehouses).filter(Warehouses.product_id == form.product_id).first():
                raise HTTPException(status_code=400, detail="Bunday product allaqachon bazada bor uni yangilashingiz mumkin")
    new_warehouse_db = Warehouses(
        name=form.name,
        product_id=form.product_id,
        quantity=form.quantity,
        price=form.price,
        branch_id=form.branch_id
    )
    save_in_db(db,new_warehouse_db)
    for i in form.phones:
        comment = i.comment
        if db.query(Phones).filter(Phones.number == i.number).first():
                    raise HTTPException(status_code=400, detail="Bu malumotlar allaqachon bazada bor")
        else:
            number = i.number
            name = i.name
            create_phone(name,comment, number, new_warehouse_db.id, thisuser.id, db, 'warehouses',thisuser.branch_id)


def update_warehouse_e(form, db, thisuser):
    if get_in_db(db, Warehouses, form.id) is None\
            or get_in_db(db, Phones, form.phones[0].id) is None:
        raise HTTPException(status_code=400, detail="Warehouse or Phone not found!")

    db.query(Warehouses).filter(Warehouses.id == form.id).update({
        Warehouses.id: form.id,
        Warehouses.name: form.name,
        Warehouses.product_id: form.product_id,
        Warehouses.quantity: form.quantity,
        Warehouses.price: form.price,
        Warehouses.branch_id: form.branch_id
    })
    db.commit()

    for i in form.phones:
        phone_id = i.id
        comment = i.comment
        number = i.number
        update_phone(phone_id, comment, number, form.id, thisuser.id, db, 'warehouses',form.branch_id)






