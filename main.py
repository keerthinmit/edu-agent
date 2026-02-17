from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to MongoDB Atlas (we’ll add MONGO_URI later)
MONGO_URI =  "mongodb+srv://<keerthi>:<mypassword123>@cluster0.jzchadb.mongodb.net/edu_database?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["edu_database"]
courses = db["courses"]
students = db["students"]

@app.get("/")
def home():
    return {"message": "Educational Agent is running!"}

@app.get("/add_course")
def add_course(name: str, duration: int):
    courses.insert_one({"name": name, "duration": duration})
    return {"status": "Course added"}

@app.get("/add_student")
def add_student(name: str, progress: int):
    students.insert_one({"name": name, "progress": progress})
    return {"status": "Student added"}

@app.get("/recommend/{student_name}")
def recommend(student_name: str):
    student = students.find_one({"name": student_name})
    if not student:
        return {"error": "Student not found"}
    if student["progress"] < 50:
        course = courses.find_one(sort=[("duration", 1)])
    else:
        course = courses.find_one(sort=[("duration", -1)])
    if course:
        return {"recommendation": f"Take {course['name']} next"}
    return {"error": "No courses available"}
