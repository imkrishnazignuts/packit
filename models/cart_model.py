from sqlalchemy import String,ForeignKey,Column
from config.database import Base

class Cart(Base):
    __tablename__ = 'carts'

    id =Column(String,primary_key=True)
    user_id = Column(String,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    warehouse_id = Column(String,ForeignKey("warehouses.id",ondelete="CASCADE"))
