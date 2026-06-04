from fastapi import APIRouter,HTTPException,Depends
from security.auth import get_current_user
from config.database import get_db
from sqlalchemy.orm import Session
from models.product_warehouse_model import ProductWarehouse
from models.user_model import User
from api.orders.order_api import get_all_orders
from services.llm_service import ai_suggessions
from api.warehouse.warehouse_api import get_warehouse_products
router = APIRouter(
    prefix='/ai',
    tags=['Ai related']
)

@router.get('/sugeestions')
def give_suggesstions(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user:
        db_user = db.query(User).where(User.id == user['id']).first()
        
        db_products = get_warehouse_products(id=db_user.warehouse_id,user=user,db=db)

        db_orders = get_all_orders(user=user,db=db)

        return ai_suggessions(products=db_products,orders=db_orders)