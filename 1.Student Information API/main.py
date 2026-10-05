from fastapi import FastAPI, Path, HTTPException,Query,Body
import json

app = FastAPI()

def load_data():

    with open("students.json","r") as f:
        data =json.load(f)
    return data

def save_data(data):
    with open("students.json","w") as f:
        json.dump(data,f)

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

def individual_student_info(student_id: str = Path(..., description="Student id of the student", example="S001")):
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

@app.post("/add_student")

def add_student(student: dict=Body()):
    data=load_data()
    std_id=student.get("id")
    data[std_id]=student
    del data[std_id]["id"]
    save_data(data)
    return {"message":"Student information added successfully"}
