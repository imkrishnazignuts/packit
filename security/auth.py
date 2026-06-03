from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from pydantic_schema.token_schema import Token
from datetime import timedelta
import datetime
from models.user_model import User
from jose import jwt,JWTError
from dotenv import load_dotenv
import os
load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['Auth related']
)

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')
pwd_context = CryptContext(schemes=['Bcrypt'],deprecated="auto")

@router.post('/token',response_model=Token)
def get_token(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user = authenticate_user(user.username,user.password,db)

    token = make_token(user.username,user.id,user.role,timedelta(minutes=10))

    return Token(access_token=token,type='Bearer')

def authenticate_user(username:str,password:str,db:Session):
    db_user = db.query(User).where(User.username == username).first()

    if not db_user:
        raise HTTPException(detail="No user found",status_code=404)
    
    if not pwd_context.verify(password,db_user.password):
        raise HTTPException("Password incorrect ",status_code=403)
    
    return db_user

def make_token(username:str,id:str,role:str,expire):
    to_encode = {'sub':id,'username':username,'role':role}
    to_encode.update({'exp': datetime.datetime.utcnow() + expire})
    return jwt.encode(to_encode,os.getenv('SECRET_KEY'),algorithm=os.getenv('ALGORITHM'))

def get_current_user(token:str=Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token=token,key=os.getenv("SECRET_KEY"),algorithms=[os.getenv('ALGORITHM')])
        id = payload['sub']
        username = payload['username']
        role = payload['role']
        return {'username':payload['username'],'id':payload['sub'],'role':payload['role']}
    except JWTError:
        raise HTTPException(detail='Authentication failed',status_code=403)