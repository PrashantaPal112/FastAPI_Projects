from fastapi import FastAPI, Path, HTTPException,Query,Body
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Optional


app = FastAPI()

def load_data():

    with open("students.json","r") as f:
        data =json.load(f)
    return data

def save_data(data):
    with open("students.json","w") as f:
        json.dump(data,f)


#Class for create new Student information with data validation using Pydantic
class Student(BaseModel):
    id: Annotated[Optional[str], Field(default=None)]
    name: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, description="Age of the student", example=[15])]
    class_: Annotated[Optional[str], Field(default=None, alias="class")]
    roll: Annotated[Optional[int], Field(default=None, gt=0, description="Roll number of the student", example=[10])]
    math_marks: Annotated[Optional[int], Field(default=None, gt=0, lt=101, alias="Math marks")]
    english_marks: Annotated[Optional[int], Field(default=None, gt=0, lt=101, alias="English marks")]
    science_marks: Annotated[Optional[int], Field(default=None, gt=0, lt=101, alias="Science marks")]


#Class for update student
class UpdateStudent(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description="Name of the student", example=["John Doe"])]
    age: Annotated[Optional[int], Field(default=None, gt=0, description="Age of the student", example=[15])]
    class_: Annotated[Optional[str], Field(default=None, alias="class")]
    roll: Annotated[Optional[int], Field(default=None, gt=0, description="Roll number of the student", example=[10])]
    math_marks: Annotated[Optional[int], Field(default=None, gt=0, lt=101, alias="Math marks")]
    english_marks: Annotated[Optional[int], Field(default=None, gt=0, lt=101, alias="English marks")]
    science_marks: Annotated[Optional[int], Field(default=None, gt=0, lt=101, alias="Science marks")]
@app.get("/")
def main_page():
    return "Student management API system"

@app.get("/student_information")
def student_info():
    data=load_data()
    return data

#PATH PARAMETER API 

# @app.get("/student_information/{student_id}")

# def individual_student_info(student_id:str):
#     data=load_data()

#     if student_id in data:
#         return data[student_id]
#     else:
#         return "Student information is not found"

# PATH FUNCTIONALITY API

@app.get("/student_information/{student_id}")

def individual_student_info(student_id: str = Path(..., description="Student id of the student", examples=["S001"])):
    data=load_data()

    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code=404, detail="Student information is not found")

#QUERY PARAMETER API

@app.get("/sort")

def student_info_by_query(sorted_by: str = Query(..., description="Sort on the basis of parameters"),order:str=Query('asc',description="Order of sorting")):

    valid_parameters=["age","class","roll","Math marks","English marks","Science marks"]

    if sorted_by not in valid_parameters:
        raise HTTPException(status_code=404, detail=f"Invalid parameter for sorting,Enter valid parametes from{valid_parameters}")

    data=load_data()
    sorted_data=list(data.values())
    sorted_data.sort(key=lambda x:x[sorted_by], reverse=(order=='desc'))
    return sorted_data

# POST request without data validation

# @app.post("/add_student")

# def add_student(student: dict=Body()):
#     data=load_data()
#     std_id=student.get("id")
#     data[std_id]=student
#     del data[std_id]["id"]
#     save_data(data)
#     return {"message":"Student information added successfully"}

# POST request with data validation

@app.post("/add_student")

def add_student(student: Student):          # input student is the objective of Student class 
    data=load_data()
    std_id=student.id
    data[std_id]=student.model_dump(by_alias=True)  # model_dump() method is used to convert the Pydantic model instance into a dictionary representation.
    del data[std_id]["id"]
    save_data(data)
    return {"message":"Student information added successfully"}


#Update Student Information API
@app.put("/student_information/{student_id}")

def update_student_info(student_id: str, student: UpdateStudent):
    data=load_data()

    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student information is not found")

    data[student_id].update(student.model_dump(exclude_unset=True, by_alias=True))  # exclude_unset=True means only the fields that have been explicitly set in the UpdateStudent model will be included in the update. Fields that are not provided will be excluded from the update operation.
    save_data(data)
    return {"message":"Student information updated successfully"}


@app.delete("/student_information/{student_id}")

def delete_student_info(student_id: str):
    data=load_data()
    if student_id not in data:
        raise HTTPException(status_code=404, detail="Student information is not found")
    del data[student_id]
    save_data(data)
    return JSONResponse(content={"message":"Student information deleted successfully"}, status_code=200)
       