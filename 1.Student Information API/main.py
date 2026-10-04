from fastapi import FastAPI, Path, HTTPException
import json

app = FastAPI()

def load_data():

    with open("students.json","r") as f:
        data =json.load(f)
    return data

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