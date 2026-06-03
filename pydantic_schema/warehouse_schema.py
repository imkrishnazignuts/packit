from pydantic import BaseModel

class warehouseCreateSchema(BaseModel):
    city:str

class warehouseResponseSchema(BaseModel):
    id:str
    city:str

