from fastapi import FastAPI
from pymongo import MongoClient
from bson.json_util import dumps
import json

app = FastAPI()

# Connect to MongoDB Atlas
# Replace <keerthi> and <mypassword123> with your actual Atlas username/password
client = MongoClient("mongodb+srv://keerthi:mypassword123@cluster0.jzchadb.mongodb.net/edu_database?retryWrites=true&w=majority")
db = client["edu_database"]
students_collection = db["students"]
courses_collection = db["courses"]

@app.get("/")
def home():
    return {"message": "Educational Agent Backend with MongoDB is running!"}

# Add a course
@app.get("/add_course")
def add_course(name: str, duration: int):
    course = {"name": name, "duration": duration}
    courses_collection.insert_one(course)
    return {"status": "Course added", "course": name, "duration": duration}

# Add a student
@app.get("/add_student")
def add_student(name: str, progress: int):
    student = {"name": name, "progress": progress}
    students_collection.insert_one(student)
    return {"status": "Student added", "student": name, "progress": progress}

# Get recommendation for a student
@app.get("/recommend/{name}")
def recommend(name: str):
    student = students_collection.find_one({"name": name})
    if not student:
        return {"error": "Student not found"}

    progress = student["progress"]
    courses = list(courses_collection.find({}))

    if not courses:
        if progress < 40:
            return {"recommendation": "Focus on basics first (Beginner courses)"}
        elif progress < 70:
            return {"recommendation": "Try intermediate courses to strengthen skills"}
        elif progress < 90:
            return {"recommendation": "Advance to specialized topics"}
        else:
            return {"recommendation": "Explore advanced projects or mentoring others"}

    # Dynamic recommendation using courses
    if progress < 40:
        course = min(courses, key=lambda c: c["duration"])
        return {"recommendation": f"Start with '{course['name']}' to build fundamentals"}
    elif progress < 70:
        sorted_courses = sorted(courses, key=lambda c: c["duration"])
        mid_index = len(sorted_courses) // 2
        course = sorted_courses[mid_index]
        return {"recommendation": f"Take '{course['name']}' to strengthen your skills"}
    elif progress < 90:
        course = max(courses, key=lambda c: c["duration"])
        return {"recommendation": f"Advance with '{course['name']}' for deeper knowledge"}
    else:
        course = max(courses, key=lambda c: c["duration"])
        return {"recommendation": f"Master '{course['name']}' and explore projects"}

# Get all courses
@app.get("/courses")
def get_courses():
    courses = list(courses_collection.find({}, {"_id": 0}))
    return courses

# Get all students
@app.get("/students")
def get_students():
    students = list(students_collection.find({}, {"_id": 0}))
    return students
