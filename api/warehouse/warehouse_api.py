from fastapi import Depends,HTTPException,APIRouter
from security.auth import get_current_user
from config.database import get_db
from sqlalchemy.orm import Session
from models.product_warehouse_model import ProductWarehouse
from models.product_model import Product
from pydantic_schema.product_schema import productResponse
from uuid import uuid4
from models.warehouse_model import Warehouse
router = APIRouter(
    prefix='/warehouse',
    tags=['Warehouse related']
)

@router.get('/{id}/products',response_model=list[productResponse])
def get_warehouse_products(id:str,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):    
    if user:
        db_warehouse = db.query(Warehouse).where(Warehouse.id == id).first()
        if not db_warehouse:
            raise HTTPException(detail="Invalid warehouse ID",status_code=404)
        products = db.query(ProductWarehouse).where(ProductWarehouse.warehouse_id == id).all()
        producst_dict = []
        for row in products:
            product = db.query(Product).where(Product.id == row.product_id).first()
            producst_dict.append(product)
        return producst_dict
    else:
        raise HTTPException(detail='Unauthenticated access',status_code=403)
    
@router.post('/{wid}/add/{pid}')
def add_product_to_warehouse(wid:str,pid:str,quantity:int,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user['role'] == 'Seller':
        if quantity>100:
            raise HTTPException(detail='sorrt Too much quantity for our site ',status_code=400)
        if quantity<=0:
            raise HTTPException(detail='quantity cant be negative ',status_code=400)
        
        db_product = db.query(Product).where(Product.id == pid).first()

        if not db_product:
            raise HTTPException(detail='Invalid product id',status_code=400)
        
        db_warehouse = db.query(Warehouse).where(Warehouse.id == wid).first()

        if not Warehouse:
            raise HTTPException(detail='Invalid Warehouse id',status_code=403)
        
        if user['id'] != db_product.user_id:
            raise HTTPException(detail='Product is not listed by you',status_code=403)
        db_product_warehouse = ProductWarehouse(id=str(uuid4()),product_id=db_product.id,quantity=quantity,warehouse_id=wid)
        db.add(db_product_warehouse)
        db.commit()
        db.refresh(db_product_warehouse)
        return db_product_warehouse
    else:
        raise HTTPException(detail='unauthenticatd access',status_code=403)
    
        
        
    