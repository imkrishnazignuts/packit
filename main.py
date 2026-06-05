from fastapi import FastAPI
from config.database import Base,engine
from models import order_model, order_product_model,product_model,product_warehouse_model,user_model,warehouse_model,cart_model,cart_product
from dotenv import load_dotenv
import os
from api.user.user_api import router as user_router
from api.product.product_api import router as product_router
from api.orders.order_api import router as order_router
from security.auth import router as auth_router
from api.cart.cart_api import router as cart_router
from api.warehouse.warehouse_api import router as warehouse_router
from api.checkout.checkout_api import router as checkout_router
from api.ai.ai_api import router as ai_router
from api.search.search_api import router as search_router
load_dotenv()

user_model.Base.metadata.create_all(engine)
product_model.Base.metadata.create_all(engine)
warehouse_model.Base.metadata.create_all(engine)
product_warehouse_model.Base.metadata.create_all(engine)
order_model.Base.metadata.create_all(engine)
order_product_model.Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(product_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(cart_router)
app.include_router(warehouse_router)
app.include_router(checkout_router)
app.include_router(ai_router)
app.include_router(search_router)
@app.get('/')
def root():
    print(os.getenv('DATABASE_URL'))
    return "welcome to backend  please add /docs after url "
