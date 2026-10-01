from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv

from app.database import init_db
from app.routes import router

# Load environment variables
load_dotenv()

# Initialize FastAPI App
app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator",
    description="Web application that generates personalized 7-day workout plans and nutrition advice using Google Gemini models.",
    version="1.0.0"
)

# Setup Base and Static directories
BASE_DIR = Path(__file__).resolve().parent.parent
static_dir = BASE_DIR / "static"
static_dir.mkdir(parents=True, exist_ok=True)
images_dir = static_dir / "images"
images_dir.mkdir(parents=True, exist_ok=True)

# Mount Static Files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Startup Event: Initialize SQLite Database & Tables
@app.on_event("startup")
def on_startup():
    init_db()

# Include Application Routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
