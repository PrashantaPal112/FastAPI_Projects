from fastapi import FastAPI,APIRouter, HTTPException,Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Annotated,Optional
from sqlalchemy.orm import Session
from model import Users
from database import engine,sessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import jwt, JWTError
from Router.auth import get_current_user
from model import Todo,Users


router=APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db            # yield will return the value
    finally:
        db.close()
db_dependency = Annotated[Session,Depends(get_db)] 
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/admin/todos")
def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get("role") not in ["admin", "Admin"]:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(Todo).all()  # want to see all values in Todo table


@router.delete("/admin/todo/{todo_id}")

def delete_todo_by_admin(user: user_dependency,db: db_dependency, todo_id:int):

    if user is None or user.get("role") not in ["admin", "Admin"]:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    specific_to= db.query(Todo).filter(Todo.id==todo_id).first()  # want to see a specific value in Todo table

    if specific_to is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todo).filter(Todo.id==todo_id).delete()
    db.commit()
    return {"detail": "Todo deleted successfully"}