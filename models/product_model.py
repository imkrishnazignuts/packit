from config.database import Base
from sqlalchemy import Column,Integer,Enum,String,CheckConstraint,ForeignKey
from typing import Optional

class Product(Base):

    __tablename__ = "products"

    id = Column(String,primary_key=True,unique=True)
    name = Column(String,nullable=False)
    price = Column(Integer)
    description = Column(String(100))
    category = Column(Enum("Snacks","Dairy","Beauty","Electronics","Bath & Body","Kitchen",name="category"),nullable=False)
    brand = Column(String,nullable=False)
    user_id = Column(String,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    __table_args__ = (
        CheckConstraint(" price>=0 AND price<=100000"),
    )

