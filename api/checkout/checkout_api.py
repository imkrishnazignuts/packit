from fastapi import APIRouter ,Depends,HTTPException
from security.auth import get_current_user
from config.database import get_db
from sqlalchemy.orm import Session
from models.cart_product import CartProduct
from models.cart_model import Cart
from models.order_model import Order
from models.order_product_model import OrderProduct
from models.user_model import User
from uuid import uuid4
router = APIRouter(
    prefix='/checkout',
    tags=['Checkout related']
)

@router.post('')
def checkout_cart(payment_type:str,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user['role'] == "Customer":
        db_user = db.query(User).where(User.id == user['id']).first()
        db_cart = db.query(Cart).where(Cart.user_id == user['id']).first()
        db_cart_product = db.query(CartProduct).where(CartProduct.cart_id == db_cart.id).all()
        if not db_cart_product:
            raise HTTPException(detail="Cart is Empty",status_code=200)
        db_order = Order(id=str(uuid4()),payment_type=payment_type,user_id=user['id'],warehouse_id=db_user.warehouse_id)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        for row in db_cart_product:
            order_product = OrderProduct(id=str(uuid4()),order_id=db_order.id,product_id=row.product_id,quantity=row.quantity)
            db.add(order_product)
            db.delete(row)
            db.commit()
        return {
            'messgae':"Order successfull",
            'order_id':db_order.id
        }
    else:
        raise HTTPException(detail='unauthenticated access',status_code=403)
    

        