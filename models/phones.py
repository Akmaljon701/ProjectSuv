from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from models.supplies import Supplies
from models.users import Users
from models.branches import Branches
from models.customers import Customers
from models.warehouse import Warehouses
from models.kassa import Kassas

class Phones(Base):
    __tablename__ = "phones"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    number = Column(String(999))
    comment = Column(String(999))
    source = Column(String(999))
    source_id = Column(Integer)
    user_id = Column(Integer)
    branch_id = Column(Integer)

    created_user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Phones.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Phones.branch_id))

    this_user = relationship('Users', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Users.id == Phones.source_id, Phones.source == "user"), backref=backref("phones"))
    
    this_branch = relationship('Branches', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Branches.id == Phones.source_id, Phones.source == "branch"), backref=backref("phones"))
    
    this_customer = relationship('Customers', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Customers.id == Phones.source_id, Phones.source == "customers"), backref=backref("phones"))
    
    this_warehouse = relationship('Warehouses', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Warehouses.id == Phones.source_id, Phones.source == "warehouses"), backref=backref("phones"))

    this_supplier = relationship('Supplies', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Supplies.id == Phones.source_id, Phones.source == "supplies"), backref=backref("phones"))
    
    this_kassa = relationship('Kassas', foreign_keys=[source_id],
                        primaryjoin=lambda: and_(Kassas.id == Phones.source_id, Phones.source == "kassa"), backref=backref("phones"))
