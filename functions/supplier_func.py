from fastapi import HTTPException
from functions.phones_func import create_phone, update_phone
from models.phones import Phones
from models.supplies import Supplies
from utils.paginatsiya import pagination,pagination2
from utils.db_operations import save_in_db,get_in_db
from sqlalchemy.orm import joinedload

def all_suppliers_r(search,limit,page,db):
    suplliers = db.query(Supplies).join(Supplies.phones).options(joinedload(Supplies.phones))
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Supplies.name.name(search_formatted))
    else:
        search_filter = Supplies.id > 0
    suplliers = suplliers.filter(search_filter).order_by(Supplies.name.asc())
    return pagination(suplliers,page,limit)

def create_supplier_r(form,db,this_user):
    if db.query(Supplies).filter(Supplies.name == form.name).first():
                raise HTTPException(status_code=400, detail="Bunday taminotchi allaqachon bazada bor")
    new_supplier = Supplies(
        name = form.name,
        product_id = form.product_id,
        quantity=form.quantity,
        price=form.price,
        date=form.date,
        user_id=this_user.id,
        branch_id=form.branch_id
    )
    save_in_db(db,new_supplier)
    for i in form.phones:
        comment = i.comment
        if db.query(Phones).filter(Phones.number == i.number).first():
                    raise HTTPException(status_code=400, detail="Bu telefon allaqachon bazada bor")
        else:
            number = i.number
            name = i.name
            create_phone(name,comment,number,new_supplier.id,this_user.id,db,"supplies",this_user.branch_id)

def update_supplier_r(form,db,this_user):
    if get_in_db(db,Supplies,form.id):
        db.query(Supplies).filter(Supplies.id == form.id).update({
            Supplies.id: form.id,
            Supplies.name: form.name,
            Supplies.product_id: form.product_id,
            Supplies.quantity: form.quantity,
            Supplies.price: form.price,
            Supplies.date: form.date,
            Supplies.user_id: this_user.id,
            Supplies.branch_id: form.branch_id
        })
        db.commit()
            
        for i in form.phones:
            phone_id = i.id
            comment = i.comment
            number = i.number
            update_phone(phone_id, comment, number, form.id, this_user.id, db, 'supplies',form.branch_id)