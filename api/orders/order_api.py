from models.order_model import Order
from pydantic_schema.order_schema import orderResponseSchema
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from security.auth import get_current_user
router = APIRouter(
    prefix='/orders',
    tags=['Order related']
)

@router.get('/',response_model=list[orderResponseSchema])
def get_all_orders(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user:
        orders = db.query(Order).where(Order.user_id == user['id']).all()
        if not orders:
            raise HTTPException(detail="No order done",status_code=200)
        return orders
    return HTTPException(detail='Unauthenticated access',status_code=403)
