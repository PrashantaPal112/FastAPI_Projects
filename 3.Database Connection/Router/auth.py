from fastapi import FastAPI,APIRouter, HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from model import Users
from database import engine,sessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import jwt
from datetime import timedelta,datetime,timezone
class usersclass(BaseModel):
    username:str
    firstname:str
    lastname:str
    email:str
    password:str
    is_active:bool
    role:str

def get_db():
    db = sessionLocal()
    try:
        yield db            # yield will return the value
    finally:
        db.close()

router=APIRouter()
db_dependency = Annotated[Session,Depends(get_db)] 

bcrypt_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY="65d17b2b8fa2188ae59133e894bda27b8540597f096153059761a5cf9c640f92"
ALGORITHM="HS256"
Outh2beare= OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username:str,password:str,db:Session):

    user=db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hash_password):
        return False
    return user

# CREATE LOG IN TOKEN FOR USER BY JWT(JESON WEB TOKEN)

def create_access_token(user_name:str,user_id:str,expires_delta:timedelta):

    encode={"sub":user_name,"id":user_id}
    expires=datetime.now(timezone.utc) + expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    

# USER INFO BY DECODING USER LOG IN TOKEN

def get_current_user(token: Annotated[str,Depends(Outh2beare)]):
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    username:str=payload.get('sub')
    user_id:int=payload.get('id')
    if username is None or user_id is None:
        return HTTPException(status_code=404,detail='User not found')
    return {'username':username, 'id':user_id}

# API FOR CREATE A NEW USER 

@router.post("/create user")
def create_user(db:db_dependency,new_user:usersclass):
    user_model=Users(
        email=new_user.email,
        username=new_user.username,
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        hash_password=bcrypt_context.hash(new_user.password),
        is_active=new_user.is_active,
        role=new_user.role
        
    ) 
    db.add(user_model)
    db.commit()
    return user_model


#LOG IN USER BY AUTHENTICATION

@router.post("/login")
def login_user(db:db_dependency,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    user=authenticate_user(form_data.username,form_data.password,db)
    if user is False:
        raise HTTPException(status_code=401,detail="Failed Authentication")
    else:
        token=create_access_token(user.username,user.id,timedelta(minutes=30))
        return {"access_token":token,"token_type":"bearer"}