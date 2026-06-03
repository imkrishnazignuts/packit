from fastapi import Depends,HTTPException,APIRouter
from security.auth import get_current_user
from config.database import get_db
from sqlalchemy.orm import Session
from models.product_warehouse_model import ProductWarehouse
from models.product_model import Product
from pydantic_schema.product_schema import productResponse
router = APIRouter(
    prefix='/warehouse',
    tags=['Warehouse related']
)

@router.get('{id}/products',response_model=list[productResponse])
def get_warehouse_products(id:str,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):    
    products = db.query(ProductWarehouse).where(ProductWarehouse.warehouse_id == id).all()
    producst_dict = []
    for row in products:
        product = db.query(Product).where(Product.id == row.product_id).first()
        producst_dict.append(product)
    return producst_dict


    