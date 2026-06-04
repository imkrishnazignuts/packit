from fastapi import APIRouter,Depends,HTTPException
from pydantic_schema.user_scema import userCreate,userResponse
from security.auth import pwd_context
from sqlalchemy.orm import Session
from config.database import get_db
from models.user_model import User
from security.auth import get_current_user
from models.warehouse_model import Warehouse
import uuid

router = APIRouter(
    prefix="/user",
    tags=['User related'])

@router.post("/create",response_model=userResponse)
def create_user(user:userCreate,db:Session=Depends(get_db)):
    db_user = db.query(User).where(User.username == user.username).first()
    
    if db_user:
        raise HTTPException(detail="User already exist",status_code=409)
    
    db_user = User(id=str(uuid.uuid4()),username=user.username,password=pwd_context.hash(user.password),email=user.email,role=user.role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post('/select/{wid}')
def select_warehouse(wid:str,user:dict=Depends(get_current_user),db:Session=Depends(get_db)):
    if user['role'] == "Customer":
        db_warehouse = db.query(Warehouse).where(Warehouse.id==wid).first()
        if not db_warehouse:
            raise HTTPException(detail="Warehouse not found",status_code=404)
        
        db_user = db.query(User).where(User.id == user['id']).first()
        db_user.warehouse_id = wid
        db.add(db_user)
        db.commit()
        raise HTTPException(detail='Warehouse changed',status_code=200)
    raise HTTPException(detail="unauthenticated access",status_code=403)





