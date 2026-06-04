from models.order_model import Order
from pydantic_schema.order_schema import orderResponseSchema
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from security.auth import get_current_user
from models.order_product_model import OrderProduct
from models.product_model import Product

router = APIRouter(
    prefix='/orders',
    tags=['Order related']
)

@router.get('/')
def get_all_orders(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user:
        orders = db.query(Order).where(Order.user_id == user['id']).all()
        if not orders:
            raise HTTPException(detail="No order done",status_code=200)
        all_order_products = []
        total=0
        for row in orders:
            per_order_product =[]
            db_order_product = db.query(OrderProduct).where(OrderProduct.order_id == row.id).all()
            for row_row in db_order_product:
                db_product = db.query(Product).where(Product.id == row_row.product_id).first()
                product_detail_in_order = {
                    'order_id':row.id,
                    'order_at':row.order_at,
                    'payment_type':row.payment_type,
                    'product':db_product,
                    'quantity':row_row.quantity,
                    'item_total':row_row.quantity*db_product.price
                }
                per_order_product.append(product_detail_in_order)
                total += (row_row.quantity*db_product.price)
            all_order_products.append(per_order_product)
            all_order_products.append({'total_bill':total})
        return all_order_products
    
