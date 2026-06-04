from pydantic import BaseModel,PastDate
from datetime import datetime
class orderCreateSchema(BaseModel):
    payment_type :str
    user_id :str
    warehouse_id:str

class orderResponseSchema(BaseModel):
    id :str
    payment_type :str
    user_id :str
    order_at :datetime
    warehouse_id:str
