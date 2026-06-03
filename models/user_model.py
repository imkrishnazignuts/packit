from sqlalchemy import Integer,String,Column,Enum,ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class User(Base):
    __tablename__ = "users"

    id=Column(String,primary_key=True)
    username=Column(String,nullable=False)
    password=Column(String,nullable=False)
    email = Column(String,unique=True)
    role = Column(Enum("Customer","Seller",name="role"),nullable=False)
    warehouse_id = Column(String,ForeignKey("warehouses.id"),nullable=True)
    orders = relationship("Order",back_populates="user")



    

    


