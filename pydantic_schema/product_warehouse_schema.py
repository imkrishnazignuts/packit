from pydantic import BaseModel

class productWarehouseCreate(BaseModel):
    product_id :str
    warehouse_id :str
    quantity:int

class productWarehouseResponse(BaseModel):
    id:str
    product_id :str
    warehouse_id :str
    quantity:int