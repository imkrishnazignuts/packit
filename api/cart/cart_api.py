from fastapi import Depends,APIRouter,HTTPException
from security.auth import get_current_user
from config.database import get_db
from sqlalchemy.orm import Session
from models.cart_model import Cart
from models.cart_product import CartProduct
from models.product_warehouse_model import ProductWarehouse
from models.user_model import User
from models.cart_product import CartProduct
from models.product_model import Product
import uuid
router=APIRouter(
    prefix='/cart',
    tags=['Cart related']
)

@router.get('')
def get_cart(user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user:
        cart = db.query(Cart).where(Cart.user_id == user['id']).first()
        if not cart:
            raise HTTPException(detail='Cart is empty',status_code=200)
        
        db_cart_product = db.query(CartProduct).where(CartProduct.cart_id == cart.id).all()
        if not db_cart_product:
            raise HTTPException(detail="Cart is empty",status_code=200)
        db_items = []
        for row in db_cart_product:
            product = db.query(Product).where(Product.id==row.product_id).first()
            item = {
                'product':product,
                'quantity':row.quantity
            }
            db_items.append(item)
        return db_items
    raise HTTPException(detail='Authentication failed',status_code=403)



@router.post('/{pid}')
def add_to_cart(pid:str,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user:
        db_product_warehouse = db.query(ProductWarehouse).where(ProductWarehouse.product_id == pid).first()
        if not db_product_warehouse:
            raise HTTPException(detail="Product is not available",status_code=400)
        
        if db_product_warehouse.quantity == 0:
            raise HTTPException(detail="Product Out of stock",status_code=404)
        db_user = db.query(User).where(User.id == user['id']).first()

        if db_product_warehouse.warehouse_id != db_user.warehouse_id:
            raise HTTPException(detail="Sorry not available in your area",status_code=400)
                
        db_cart = db.query(Cart).where(Cart.user_id == user['id']).first()
        
        if not db_cart:
            db_cart = Cart(id=str(uuid.uuid4()),user_id=user['id'],warehouse_id=db_user.warehouse_id)
            db.add(db_cart)
            db.commit()
        
        if db_cart.warehouse_id != db_user.warehouse_id:
            raise HTTPException(detail="Cart Contains different warehouse products",status_code=400)
        
        cart_product = db.query(CartProduct).where(CartProduct.product_id == pid).first()
        
        if not cart_product:
            cart_product = CartProduct(id=str(uuid.uuid4()),product_id=pid,cart_id=db_cart.id,quantity=0)
        
        if db_product_warehouse ==0:
            raise HTTPException(detail="Stock not available",status_code=200)
        
        cart_product.quantity +=1
        db_product_warehouse.quantity-=1
        db.add(cart_product)
        db.add(db_product_warehouse)
        db.commit()
        db.refresh(cart_product)
        return cart_product

@router.delete('/{pid}')
def remove_from_cart(pid:str,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user:
        db_product_warehouse = db.query(ProductWarehouse).where(ProductWarehouse.product_id == pid).first()

        if not db_product_warehouse:
            raise HTTPException(detail="Product not available",status_code=400)
         
        db_user = db.query(User).where(User.id == user['id']).first()

        db_cart = db.query(Cart).where(Cart.user_id == user['id']).first()
        
        if not db_cart:
            db_cart = Cart(id=str(uuid.uuid4()),user_id=user['id'],warehouse_id=db_user.warehouse_id)
            db.add(db_cart)
            db.commit()
        
        if db_cart.warehouse_id != db_user.warehouse_id:
            raise HTTPException(detail="Cart Contains different warehouse products",status_code=400)
        
        cart_product = db.query(CartProduct).where(CartProduct.product_id == pid).first()
        
        if not cart_product:
            raise HTTPException(detail="Item is not In Cart",status_code=404)
                

        if(cart_product.quantity == 1):
            db.delete(cart_product)
            db.commit()
            raise HTTPException(detail="Item Removed From Cart",status_code=203)
        
        
        cart_product.quantity -=1
        db_product_warehouse.quantity+=1

        db.add(cart_product)
        db.add(db_product_warehouse)
        db.commit()
        db.refresh(cart_product)
        return cart_product