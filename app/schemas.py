from pydantic import BaseModel, Field, field_validator
from typing import Optional

class UserInput(BaseModel):
    username: str = Field(..., min_length=1, description="User's full name or username")
    user_id: str = Field(..., min_length=1, description="Unique User ID")
    age: int = Field(..., gt=0, lt=120, description="Age in years")
    weight: float = Field(..., gt=0, description="Weight in kg")
    goal: str = Field(..., min_length=1, description="Fitness goal (e.g., Weight Loss, Muscle Gain, General Wellness)")
    intensity: str = Field(..., min_length=1, description="Workout intensity (Low, Medium, High)")

    @field_validator('username', 'user_id', 'goal', 'intensity')
    @classmethod
    def check_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace only.")
        return v.strip()


class FeedbackRequest(BaseModel):
    user_id: str = Field(..., min_length=1, description="User ID for plan lookup")
    feedback: str = Field(..., min_length=1, description="User feedback for plan modification")

    @field_validator('user_id', 'feedback')
    @classmethod
    def check_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace only.")
        return v.strip()


class UserPlanResponse(BaseModel):
    id: int
    user_id: str
    username: str
    age: int
    weight: float
    goal: str
    intensity: str
    original_plan: str
    nutrition_tip: str
    updated_plan: Optional[str] = None
    feedback: Optional[str] = None

    class Config:
        from_attributes = True
