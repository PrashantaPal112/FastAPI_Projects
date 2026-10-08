from database import Base

from sqlalchemy import Column, Integer, String, Boolean

class Todo(Base):
    __tablename__= "todos"
    id= Column(Integer,primary_key=True,index=True)
    title= Column(String,nullable=False)
    description= Column(String,nullable=True)
    priority= Column(Integer,nullable=False)
    completed= Column(Boolean,default=False)