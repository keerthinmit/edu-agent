from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Educational Agent API")

# Enable CORS (required for Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
courses = []
students = []

@app.get("/")
def root():
    return {"message": "Educational Agent backend is running!"}

# Add a course
@app.get("/add_course")
def add_course(name: str, duration: int):
    course = {"name": name, "duration": duration}
    courses.append(course)
    return {"message": "Course added successfully", "course": course}

# Add a student
@app.get("/add_student")
def add_student(name: str, progress: int):
    student = {"name": name, "progress": progress}
    students.append(student)
    return {"message": "Student added successfully", "student": student}

# Get all courses
@app.get("/courses")
def get_courses():
    return courses

# Get all students
@app.get("/students")
def get_students():
    return students

# Recommendation
@app.get("/recommend/{name}")
def recommend(name: str):
    for s in students:
        if s["name"].lower() == name.lower():
            if s["progress"] < 50:
                return {"recommendation": "Focus on fundamentals and beginner courses."}
            return {"recommendation": "You are ready for advanced courses!"}
    return {"error": "Student not found"}

# AI Assistant
@app.get("/ai_recommend")
def ai_recommend(query: str):
    q = query.lower()
    if "python" in q:
        return {"answer": "I recommend 'Python Basics' for 30 days."}
    if "java" in q:
        return {"answer": "Start with 'Java Fundamentals'."}
    if "data" in q:
        return {"answer": "Try 'Data Structures & Algorithms'."}
    return {"answer": "Explore courses based on your current progress."}