from fastapi import FastAPI

app = FastAPI()

# In-memory storage
courses = []
students = []

# Root route (so you don’t see "Not Found" at base URL)
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

# Recommendation based on progress
@app.get("/recommend/{name}")
def recommend(name: str):
    for student in students:
        if student["name"].lower() == name.lower():
            if student["progress"] < 50:
                return {"recommendation": "Focus on basics and foundational courses."}
            else:
                return {"recommendation": "You are ready for advanced courses!"}
    return {"error": "Student not found"}

# AI Assistant route
@app.get("/ai_recommend")
def ai_recommend(query: str):
    query_lower = query.lower()
    if "java" in query_lower:
        return {"answer": "I recommend starting with 'Java Basics' for 30 days."}
    elif "python" in query_lower:
        return {"answer": "Try 'Python for Beginners' — it’s great for fast progress."}
    elif "data" in query_lower:
        return {"answer": "Consider 'Data Structures and Algorithms' to strengthen your skills."}
    else:
        return {"answer": "Based on your query, I suggest reviewing your current progress and exploring a matching course."}
