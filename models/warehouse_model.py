from sqlalchemy import Integer,String,Column
from config.database import Base

class Warehouse(Base):
    __tablename__ = "warehouses"
    
    id = Column(String,primary_key=True)
    city = Column(String,nullable=False,unique=True)

