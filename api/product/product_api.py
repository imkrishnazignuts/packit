from models.product_model import Product
from pydantic_schema.product_schema import productResponse,productCreate
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from security.auth import get_current_user
from config.database import get_db
from uuid import uuid4
router = APIRouter(
    prefix='/products',
    tags=['Product related']
)

@router.get('/',response_model=list[productResponse])
def get_all_products(db:Session=Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(detail="No product listed",status_code=200)
    return products

@router.post('/add',response_model=productResponse)
def add_product(product:productCreate,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user:
        if user["role"]=="Seller":
            if product.price >=100000 or product.price<=0:
                raise HTTPException(detail="Please check price",status_code=200)

            db_product = Product(id=str(uuid4()),name=product.name,price=product.price,description=product.description,category=product.category,brand=product.brand,user_id= user['id'])
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return db_product
        raise HTTPException(detail='Unauthenticated access',status_code=403)

@router.delete('/delete/{id}')
def delete_product(id:str,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user:
        if user['role'] == "Seller":
            db_product = db.query(Product).where(Product.id == id).first()
            if not db_product:
                raise HTTPException(detail="No Product found",status_code=404)
            if db_product.user_id != user['id']:
                raise HTTPException(detail="unauthenticated Deletion",status_code=403)
            db.delete(db_product)
            db.commit()
            return {'msg':'Deleted successfully'}
        else:
            raise HTTPException(detail="unauthenticated access",status_code=403)
    else:
        raise HTTPException(detail='Login first',status_code=403)       

@router.get('/{id}',response_model=productResponse)
def get_perticular_product(id:str,db:Session=Depends(get_db)):
    db_product = db.query(Product).where(Product.id == id).first()
    if not db_product:
        raise HTTPException(detail="Product not found",status_code=404)
    return db_product