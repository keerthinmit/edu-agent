from fastapi import FastAPI
app = FastAPI()

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

# Initialize FastAPI app
app = FastAPI(title="EduAgent Backend", description="AI-powered learning assistant")

# Allow frontend (Netlify) to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For security, replace "*" with your Netlify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI securely (use environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "EduAgent backend is running!"}

# --- AI Assistant ---
@app.get("/ask_ai")
async def ask_ai(query: str = Query(..., description="User question")):
    """
    Chat with AI assistant (EduAgent).
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",   # or "gpt-4" if available
            messages=[
                {"role": "system", "content": "You are EduAgent, a helpful AI tutor."},
                {"role": "user", "content": query}
            ],
            max_tokens=200,
            temperature=0.7
        )
        answer = response["choices"][0]["message"]["content"]
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}

# --- Course Recommendation Engine ---
@app.get("/recommend_courses")
async def recommend_courses(student_name: str, progress: int):
    """
    Recommend next courses/topics based on student progress.
    """
    try:
        prompt = f"""
        A student named {student_name} has {progress}% progress in their current course.
        Suggest 2-3 next courses or topics they should study, with short explanations.
        Keep it motivational and concise.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are EduAgent, an AI that recommends learning paths."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.8
        )
        recommendations = response["choices"][0]["message"]["content"]
        return {"recommendations": recommendations}
    except Exception as e:
        return {"recommendations": f"Error: {str(e)}"}

# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "EduAgent backend is running!"}
