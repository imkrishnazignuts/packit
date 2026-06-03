from sqlalchemy import Column,Integer,String,CheckConstraint,ForeignKey
from config.database import Base

class OrderProduct(Base):
    __tablename__ = "order_product"
    
    id = Column(String,primary_key=True)
    order_id = Column(String,ForeignKey("orders.id",ondelete="CASCADE"),nullable=False)
    product_id = Column(String,ForeignKey("products.id",ondelete="CASCADE"),nullable=False)
    quantity = Column(Integer,nullable=False)

    __table_args__ = (
        CheckConstraint(" quantity>=0 AND quantity<=100"),
    )