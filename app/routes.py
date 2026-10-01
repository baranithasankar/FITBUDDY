import markdown
from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pathlib import Path
from pydantic import ValidationError

from app.database import get_db, save_plan, update_plan, get_user, get_all_users
from app.models import UserPlan
from app.schemas import UserInput, FeedbackRequest
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()

# Templates directory setup
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def render_md(text: str) -> str:
    """Helper to convert Markdown text to HTML safely."""
    if not text:
        return ""
    return markdown.markdown(text, extensions=['fenced_code', 'tables', 'nl2br'])

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """GET / - Render homepage with workout generator form."""
    return templates.TemplateResponse(request=request, name="index.html")


@router.post("/generate-workout", response_class=HTMLResponse)
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):
    """POST /generate-workout - Process user input, generate plan & tip, store in DB, render result."""
    try:
        # Pydantic schema validation
        user_data = UserInput(
            username=username,
            user_id=user_id,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )
    except ValidationError as e:
        error_msgs = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": f"Invalid input data: {', '.join(error_msgs)}",
                "form_data": {
                    "username": username,
                    "user_id": user_id,
                    "age": age,
                    "weight": weight,
                    "goal": goal,
                    "intensity": intensity
                }
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # 1. Call Gemini workout generator (structured 7-day workout)
    workout_plan_raw = generate_workout_gemini(
        username=user_data.username,
        user_id=user_data.user_id,
        age=user_data.age,
        weight=user_data.weight,
        goal=user_data.goal,
        intensity=user_data.intensity
    )

    # 2. Call Gemini flash generator (nutrition / recovery tip)
    nutrition_tip_raw = generate_nutrition_tip_with_flash(
        goal=user_data.goal,
        intensity=user_data.intensity,
        age=user_data.age,
        weight=user_data.weight
    )

    # 3. Store in database
    user_plan = save_plan(
        db=db,
        user_id=user_data.user_id,
        username=user_data.username,
        age=user_data.age,
        weight=user_data.weight,
        goal=user_data.goal,
        intensity=user_data.intensity,
        original_plan=workout_plan_raw,
        nutrition_tip=nutrition_tip_raw
    )

    # Render result page with HTML formatted text
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": user_plan.username,
            "user_id": user_plan.user_id,
            "age": user_plan.age,
            "weight": user_plan.weight,
            "goal": user_plan.goal,
            "intensity": user_plan.intensity,
            "workout_plan": workout_plan_raw,
            "workout_plan_html": render_md(workout_plan_raw),
            "nutrition_tip": nutrition_tip_raw,
            "nutrition_tip_html": render_md(nutrition_tip_raw),
            "updated_plan": user_plan.updated_plan,
            "updated_plan_html": render_md(user_plan.updated_plan) if user_plan.updated_plan else None,
            "feedback": user_plan.feedback
        }
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):
    """POST /submit-feedback - Receive feedback, modify plan with Gemini, preserve original plan, store updated plan."""
    try:
        feedback_data = FeedbackRequest(user_id=user_id, feedback=feedback)
    except ValidationError as e:
        error_msgs = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "error": f"Invalid feedback submission: {', '.join(error_msgs)}",
                "user_id": user_id
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user_plan = get_user(db, feedback_data.user_id)
    if not user_plan:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "error": f"User ID '{feedback_data.user_id}' not found in database. Please generate a workout plan first."
            },
            status_code=status.HTTP_404_NOT_FOUND
        )

    user_info = {
        "username": user_plan.username,
        "age": user_plan.age,
        "weight": user_plan.weight,
        "goal": user_plan.goal,
        "intensity": user_plan.intensity
    }

    updated_plan_raw = update_workout_plan(
        original_plan=user_plan.original_plan,
        feedback=feedback_data.feedback,
        user_info=user_info
    )

    user_plan = update_plan(
        db=db,
        user_id=feedback_data.user_id,
        updated_plan=updated_plan_raw,
        feedback=feedback_data.feedback
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "username": user_plan.username,
            "user_id": user_plan.user_id,
            "age": user_plan.age,
            "weight": user_plan.weight,
            "goal": user_plan.goal,
            "intensity": user_plan.intensity,
            "workout_plan": user_plan.original_plan,
            "workout_plan_html": render_md(user_plan.original_plan),
            "nutrition_tip": user_plan.nutrition_tip,
            "nutrition_tip_html": render_md(user_plan.nutrition_tip),
            "updated_plan": user_plan.updated_plan,
            "updated_plan_html": render_md(user_plan.updated_plan),
            "feedback": user_plan.feedback,
            "success_message": "Workout plan successfully updated based on your feedback!"
        }
    )


@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(request: Request, db: Session = Depends(get_db)):
    """GET /view-all-users - Admin page displaying all registered users and their plans."""
    users = get_all_users(db)

    for u in users:
        u.original_plan_html = render_md(u.original_plan)
        u.updated_plan_html = render_md(u.updated_plan) if u.updated_plan else None
        u.nutrition_tip_html = render_md(u.nutrition_tip) if u.nutrition_tip else None

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users
        }
    )
