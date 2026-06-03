from pydantic import BaseModel

class orderCreateSchema(BaseModel):
    payment_type :str
    user_id :str
    warehouse_id:str

class orderResponseSchema(BaseModel):
    id :str
    payment_type :str
    user_id :str
    order_at :str
    warehouse_id:str
