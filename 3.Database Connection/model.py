from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

class Todo(Base):
    __tablename__= "todos"
    id= Column(Integer,primary_key=True,index=True)
    title= Column(String,nullable=False)
    description= Column(String,nullable=True)
    priority= Column(Integer,nullable=False)
    completed= Column(Boolean,default=False)
    owner_id=Column(Integer,ForeignKey("users.id"))  # this will be used to link the todo with the user who created it


class Users(Base):
    __tablename__= "users"
    id= Column(Integer,primary_key=True,index=True)
    username= Column(String,nullable=False,unique=True) 
    firstname= Column(String,nullable=False)
    lastname= Column(String,nullable=False)
    email= Column(String,nullable=False,unique=True)
    hash_password= Column(String,nullable=False)
    is_active= Column(Boolean,default=True)
    role= Column(String,nullable=False)