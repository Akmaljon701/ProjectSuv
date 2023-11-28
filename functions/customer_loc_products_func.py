from utils.db_operations import save_in_db, get_in_db
from utils.paginatsiya import pagination
from models.customer_loc import Customer_loc_products



def all_customer_loc_products(search, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = (Customer_loc_products.name.like(search_formatted))
    else:
        search_filter = Customer_loc_products.id > 0
    customer_loc_products = db.query(Customer_loc_products).filter(search_filter).order_by(Customer_loc_products.name.asc())
    return pagination(customer_loc_products, page, limit)


def create_customer_loc_product_y(form, db,this_user):
    new_customer_loc_product = Customer_loc_products(
        name = form.name,
        customer_loc_id=form.customer_loc_id,
        quantity=form.quantity,
        product_id=form.product_id,
        user_id=this_user.id,
        branch_id=form.branch_id
    )
    save_in_db(db, new_customer_loc_product)


def update_customer_loc_product_y(form,db,this_user):
    if get_in_db(db,Customer_loc_products, form.id):
        db.query(Customer_loc_products).filter(Customer_loc_products.id == form.id).update({
            Customer_loc_products.id: form.id,
            Customer_loc_products.name: form.name, 
            Customer_loc_products.quantity : form.quantity,
            Customer_loc_products.product_id : form.product_id,
            Customer_loc_products.user_id : this_user.id
        })
        db.commit()

