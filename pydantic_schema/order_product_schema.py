from pydantic import BaseModel

class orderProductSchema(BaseModel):
    
    id :str
    order_id :str
    product_id :str
    quntity:int