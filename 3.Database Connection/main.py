from database import engine,sessionLocal
from fastapi import FastAPI, Depends, HTTPException
import model
from model import Todo,Users
from sqlalchemy.orm import Session
from typing import Annotated,Optional
from pydantic import BaseModel,Field
from Router import auth
from Router.auth import get_current_user
from Router import admin

class TodoRequest(BaseModel):
    title: str
    description: str=Field(max_length=100)  # description can be optional but should not exceed 300 characters
    priority: int=Field(gt=0, lt=6)  # priority should be between 1 and 5
    completed: bool

class UpdateTodoRequest(BaseModel):
    title: Optional[str]=Field(default=None)  # title can be optional
    description: Optional[str]=Field(default=None, max_length=100)  # description can be optional but should not exceed 300 characters
    priority: Optional[int]=Field(default=None, gt=0, lt=6)  # priority should be between 1 and 5
    completed:Optional[bool]=Field(default=None)  # completed can be optional

app=FastAPI()

model.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)  # include the auth router
app.include_router(admin.router, prefix="/auth")  # include the auth router with a prefix


def get_db():
    db = sessionLocal()
    try:
        yield db            # yield will return the value
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]  # this will create a dependency for the db session
user_dependency = Annotated[dict,Depends(get_current_user)]  # this will create a dependency for the current user

@app.get("/")

def read_db(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(model.Todo).filter(model.Todo.owner_id==user.get('id')).all()  # want to see all values in Todo table


#Show an individual todo item by id

@app.get("/todo/{todo_id}")

def read_specific_todosuser(user: user_dependency,db: db_dependency, todo_id:int):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    specific_to= db.query(Todo).filter(model.Todo.owner_id==user.get('id')).filter(Todo.id==todo_id).first()  # want to see a specific value in Todo table

    if specific_to is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    return specific_to

# @app.post("/add/")

# def new_todo(db: db_dependency, new_todo: TodoRequest):
#     todo_model=Todo(**new_todo.model_dump())  # unpacking the dictionary to create a new Todo object
#     db.add(todo_model)
#     db.commit()

#Update an existing todo item

@app.put("/update/{todo_id}")

def update_todo(user: user_dependency,db: db_dependency, todo_id:int, updated_todo: UpdateTodoRequest):

    specific_to= db.query(Todo).filter(model.Todo.owner_id==user.get('id')).filter(Todo.id==todo_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if specific_to is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data= updated_todo.model_dump(exclude_unset=True)  # get the data that has been updated

    for key, value in update_data.items():
        setattr(specific_to, key, value)

    db.commit()

    return {"detail": "Todo updated successfully"}

@app.delete("/delete/{todo_id}")

def delete_todo(user: user_dependency,db: db_dependency, todo_id:int):
    specific_to= db.query(Todo).filter(model.Todo.owner_id==user.get('id')).filter(Todo.id==todo_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if specific_to is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todo).filter(model.Todo.owner_id==user.get('id')).filter(Todo.id==todo_id).delete()
    db.commit()
    return {"detail": "Todo deleted successfully"}



#CREATE NEW TODO ITEM FOR A SPECIFIC USER
# NOTE: `new_todo` must be typed as `TodoRequest` (Pydantic model), NOT `Todo`
# (SQLAlchemy model). Using `Todo` here causes:
# FastAPIError: Invalid args for response field! Hint: check that <class 'model.Todo'>
# is a valid Pydantic field type.
@app.post("/add_newtodo/")

def create_user_todo(user: user_dependency,db:db_dependency, new_todo: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo_model=Todo(**new_todo.model_dump(), owner_id=user.get('id'))  # unpacking the dictionary to create a new Todo object
    db.add(todo_model)
    db.commit()
    return {"detail": "Todo created successfully"}