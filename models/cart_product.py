from sqlalchemy import String,ForeignKey,Column,Integer
from config.database import Base

class CartProduct(Base):
    __tablename__ = "cart_product"

    id=Column(String,primary_key=True)
    cart_id = Column(String,ForeignKey("carts.id",ondelete="CASCADE"),nullable=False)
    product_id = Column(String,ForeignKey("products.id",ondelete="CASCADE"),nullable=False)
    quantity = Column(Integer,nullable=False)
    