from fastapi import HTTPException
from utils.db_operations import save_in_db, get_in_db
from utils.paginatsiya import pagination
from models.products import Products


def all_products(search, page, limit, db):
    if search :
        search_formatted = "%{}%".format(search)
        search_filter = (Products.name.like(search_formatted))
    else :
        search_filter = Products.id > 0
    products = db.query(Products).filter(search_filter).order_by(Products.name.asc())
    return pagination(products, page, limit)


def create_products_y(form, db,this_user):
    if db.query(Products).filter(Products.name == form.name).first():
                raise HTTPException(status_code=400, detail="Bunday malumot allaqachon bazada bor")
    else:
        new_products_db = Products(
            name=form.name,
            comment=form.comment,
            price=form.price,
            category_id=form.category_id,
            user_id=this_user.id,
            branch_id=form.branch_id

        )
        save_in_db(db, new_products_db)


def update_products_y(form,db,this_user):
    if get_in_db(db, Products, form.id):
        db.query(Products).filter(Products.id == form.id).update({
            Products.id: form.id,
            Products.name: form.name,
            Products.comment: form.comment,
            Products.category_id: form.category_id,
            Products.branch_id: form.branch_id,
            Products.user_id: this_user.id
        })
        db.commit()

