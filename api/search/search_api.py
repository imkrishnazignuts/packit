from fastapi import FastAPI,APIRouter,Depends,HTTPException
from security.auth import get_current_user
from config.database import get_db
from sqlalchemy.orm import Session 
from models.product_warehouse_model import ProductWarehouse
from models.product_model import Product
from sqlalchemy import Cast,String

router = APIRouter(
    prefix='/search',
    tags=['Search related']
)


@router.get('')
def search_products(product_name:str=None,category:str=None,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user['role'] == 'Customer':
        searched_products = []
        if product_name and category:
            db_product = db.query(Product).filter(Cast(Product.category,String).ilike(f"%{category}%"), Product.name.ilike(f"%{product_name}%")).all()
            for row in db_product:
                db_product_available = db.query(ProductWarehouse).filter(ProductWarehouse.product_id == row.id).first()
                if db_product_available:
                    searched_products.append(row)
            
            if not searched_products:
                raise HTTPException(detail='Unavailabe in your area warehouse',status_code=200)
            return searched_products
        if product_name:
            db_product = db.query(Product).filter(Product.name.ilike(f"%{product_name}%")).all()
            if not db_product:
                raise HTTPException(detail='No product found',status_code=200)
            
            for row in db_product:
                db_product_available = db.query(ProductWarehouse).filter(ProductWarehouse.product_id == row.id).first()
                if db_product_available:
                    searched_products.append(row)
            
            if not searched_products:
                raise HTTPException(detail='Unavailabe in your area warehouse',status_code=200)
            
        if category:
            db_product = db.query(Product).filter(Cast(Product.category,String).ilike(f"%{category}%")).all()
            if not db_product:
                raise HTTPException(detail='No category found',status_code=200)
            
            for row in db_product:
                db_product_available = db.query(ProductWarehouse).filter(ProductWarehouse.product_id == row.id).first()
                if db_product_available:
                    searched_products.append(row)
            
            if not searched_products:
                raise HTTPException(detail='Unavailabe in your area warehouse',status_code=200)
        return searched_products
    else:
        raise HTTPException(detail='unauthenticated access',status_code=403)