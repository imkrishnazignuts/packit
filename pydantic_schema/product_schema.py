from pydantic import BaseModel

class productCreate(BaseModel):
    name :str
    price :int
    description :str
    category : str
    brand : str

class productResponse(BaseModel):
    id:str
    name :str
    price :int
    description :str
    category : str
    brand : str
