from models.user_products import User_products
from utils.db_operations import get_in_db, save_in_db
from utils.paginatsiya import pagination

def all_user_products(search,page,limit,db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (User_products.name.like(search_formatted))
    else:
        search_filter = User_products.id > 0
    products = db.query(User_products).filter(search_filter).order_by(User_products.name.asc())
    return pagination(products, page, limit)

def create_user_products_y(form, db,this_user):
    new_user_products_db = User_products(
        name=form.name,
        product_id=form.product_id,
        quantity=form.quantity,
        user_id=this_user.id,
        branch_id=form.branch_id

    )
    save_in_db(db, new_user_products_db)

def update_user_products_y(form,db,this_user):
    if get_in_db(db, User_products, form.id):
        db.query(User_products).filter(User_products.id == form.id).update({
            User_products.id: form.id,
            User_products.name: form.name,
            User_products.product_id: form.product_id,
            User_products.quantity: form.quantity,
            User_products.user_id: this_user.id,
            User_products.branch_id: form.branch_id
        })
        db.commit()
