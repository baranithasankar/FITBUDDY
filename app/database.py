from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

# --- Required Document CRUD Functions ---

def get_user(db: Session, user_id: str):
    """Retrieve user record by user_id."""
    from app.models import UserPlan
    return db.query(UserPlan).filter(UserPlan.user_id == user_id).first()

def get_original_plan(db: Session, user_id: str) -> Optional[str]:
    """Retrieve original workout plan for a given user_id."""
    user = get_user(db, user_id)
    return user.original_plan if user else None

def get_all_users(db: Session) -> List:
    """Retrieve all registered user records."""
    from app.models import UserPlan
    return db.query(UserPlan).order_by(UserPlan.created_at.desc()).all()

def get_all_plans(db: Session) -> List:
    """Retrieve all stored plans records."""
    return get_all_users(db)

def save_user(db: Session, user_id: str, username: str, age: int, weight: float, goal: str, intensity: str):
    """Save or update basic user profile in SQLite."""
    from app.models import UserPlan
    user = get_user(db, user_id)
    if user:
        user.username = username
        user.age = age
        user.weight = weight
        user.goal = goal
        user.intensity = intensity
    else:
        user = UserPlan(
            user_id=user_id,
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            original_plan="",
            nutrition_tip=""
        )
        db.add(user)
    db.commit()
    db.refresh(user)
    return user

def save_plan(db: Session, user_id: str, username: str, age: int, weight: float, goal: str, intensity: str, original_plan: str, nutrition_tip: str):
    """Save user details, original workout plan, and nutrition tip into SQLite."""
    from app.models import UserPlan
    user = get_user(db, user_id)
    if user:
        user.username = username
        user.age = age
        user.weight = weight
        user.goal = goal
        user.intensity = intensity
        user.original_plan = original_plan
        user.nutrition_tip = nutrition_tip
        user.updated_plan = None
        user.feedback = None
    else:
        user = UserPlan(
            user_id=user_id,
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            original_plan=original_plan,
            nutrition_tip=nutrition_tip
        )
        db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_plan(db: Session, user_id: str, updated_plan: str, feedback: str):
    """Save feedback and updated workout plan into SQLite while preserving original plan."""
    user = get_user(db, user_id)
    if user:
        user.updated_plan = updated_plan
        user.feedback = feedback
        db.commit()
        db.refresh(user)
    return user

