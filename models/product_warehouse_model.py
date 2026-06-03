from sqlalchemy import Column,Integer,Enum,String,ForeignKey
from config.database import Base

class ProductWarehouse(Base):
    __tablename__ = "product_warehouse"
    id=Column(String,primary_key=True)
    product_id = Column(String,ForeignKey("products.id",ondelete="CASCADE"),nullable=False)
    warehouse_id = Column(String,ForeignKey("warehouses.id",ondelete="CASCADE"),nullable=False)
    quantity=Column(Integer)