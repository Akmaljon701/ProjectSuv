from db import Base
from sqlalchemy import *
from sqlalchemy.orm import relationship
from models.users import Users
from models.branches import Branches
class Supplies(Base):
    __tablename__ = "supplies"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(999))
    product_id = Column(Integer)
    quantity = Column(Integer)
    price = Column(Integer)
    date = Column(DateTime)
    user_id = Column(Integer)
    branch_id = Column(Integer)

    created_user = relationship('Users', foreign_keys=[user_id],
                        primaryjoin=lambda: and_(Users.id == Supplies.user_id))

    branch = relationship('Branches', foreign_keys=[branch_id],
                             primaryjoin=lambda: and_(Branches.id == Supplies.branch_id))

    