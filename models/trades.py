from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import *
from models.branches import Branches

from models.users import Users
from models.orders import Orders
from models.warehouse import Warehouses

class Trades(Base):
    __tablename__ = "trades"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    warehouse_pr_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Numeric)
    order_id = Column(Integer)
    user_id = Column(Integer)
    branch_id = Column(Integer)

    user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Trades.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Trades.branch_id))
    
    order = relationship('Orders', foreign_keys=[order_id],
                             primaryjoin=lambda: and_(Orders.id == Trades.order_id))
    
    warehouser = relationship("Warehouses",foreign_keys=[warehouse_pr_id],
                              primaryjoin=lambda: and_(Warehouses.id == Trades.warehouse_pr_id))