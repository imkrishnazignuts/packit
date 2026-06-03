from pydantic import BaseModel
 
class userCreate(BaseModel):
    username:str
    password:str
    email:str
    role:str

class userResponse(BaseModel):
    id:str
    username:str
    email:str
    role:str


