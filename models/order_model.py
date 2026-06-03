import datetime
from sqlalchemy import Column,Integer,Enum,String,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from config.database import Base

class Order(Base):
    __tablename__ = "orders"

    id=Column(String,primary_key=True)
    payment_type = Column(Enum("Cash","Online","Netbanking",name="ptype"),nullable=False)
    user_id = Column(String,ForeignKey("users.id",ondelete="CASCADE"))
    order_at = Column(DateTime,default=datetime.datetime.utcnow,nullable=False)
    warehouse_id=Column(String,ForeignKey("warehouses.id"),nullable=False)
    user = relationship("User",back_populates="orders")
