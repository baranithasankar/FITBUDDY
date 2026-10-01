import os
from dotenv import load_dotenv

load_dotenv()

def generate_fallback_updated_plan(original_plan: str, feedback: str) -> str:
    """Fallback plan updater when Gemini API Key is missing or invalid."""
    return f"""### 🔄 Updated 7-Day Workout Plan (Feedback Applied - Demo Mode)

> **User Feedback Applied:** "{feedback}"
> *(Note: GEMINI_API_KEY is missing or invalid in `.env`. Revised demo plan incorporating your feedback below.)*

---

### **Day 1: Modified Upper Body + Added Cardio**
* **Focus:** Upper body strength with feedback adjustment ({feedback})
* **Warm-up (8 mins):** Arm swings, light jogging in place
* **Main Workout:**
  * Push-ups: 3 sets x 12 reps
  * Dumbbell Shoulder Press: 3 sets x 12 reps
  * **Cardio Addition:** 15 mins Moderate-intensity Treadmill / Jogging
* **Cool-down:** 5 mins full body stretch

---

### **Day 2: Modified Lower Body & Mobility**
* **Focus:** Leg strength & agility
* **Warm-up (8 mins):** Leg swings, bodyweight squats
* **Main Workout:**
  * Squats: 4 sets x 15 reps
  * Lunges: 3 sets x 12 reps per leg
  * Glute Bridges: 3 sets x 15 reps
* **Cool-down:** 5 mins static stretching

---

### **Day 3: Active Rest / Yoga & Stretch (Rest Day)**
* **Focus:** Rest & Active Recovery based on feedback
* **Activities:** 30 minutes light Yoga or Walk, deep breathing
* **Recovery:** Full rest, body hydration

---

### **Day 4: Core & Back Conditioning**
* **Focus:** Back strength & core balance
* **Main Workout:**
  * Bent-over rows / Resistance rows: 4 sets x 12 reps
  * Plank holds: 3 sets x 45s
  * Superman holds: 3 sets x 30s
* **Cool-down:** Cobra stretch & Child's pose

---

### **Day 5: Adjusted Cardio & Endurance Focus**
* **Focus:** Tailored cardiovascular endurance ({feedback})
* **Main Workout:**
  * 20 mins Interval Cardio (Jumping jacks, high knees)
  * Bodyweight Circuit: 3 rounds
* **Cool-down:** 5 mins calf and hamstring stretch

---

### **Day 6: Low Impact Mobility & Balance**
* **Focus:** Low intensity movement and recovery
* **Main Workout:**
  * Bodyweight lunges, side planks, leg raises
* **Cool-down:** Stretching & relaxation

---

### **Day 7: Complete Rest & Regeneration Day**
* **Focus:** Full muscular recovery and preparation for next week.
"""

def update_workout_plan(original_plan: str, feedback: str, user_info: dict = None) -> str:
    """Update existing 7-day workout plan based on user feedback using Gemini AI."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key or api_key == "your_api_key_here":
        return generate_fallback_updated_plan(original_plan, feedback)

    user_details = ""
    if user_info:
        user_details = f"User Profile: Name={user_info.get('username')}, Age={user_info.get('age')}, Weight={user_info.get('weight')}kg, Goal={user_info.get('goal')}, Intensity={user_info.get('intensity')}"

    prompt = f"""
You are FitBuddy, an expert AI fitness coach.
A user has provided feedback on their existing 7-day workout plan.

{user_details}

--- ORIGINAL WORKOUT PLAN ---
{original_plan}

--- USER FEEDBACK ---
"{feedback}"

Instructions:
1. Carefully analyze the user's feedback (e.g., "add more cardio", "include more rest days", "add yoga", "reduce intensity", "focus on upper body").
2. Revise and regenerate the full 7-Day Workout Plan (Day 1 through Day 7) incorporating all requested modifications.
3. Keep the plan structured with Day headers, Warm-up, Main Workout (Exercises, Sets, Reps/Duration, Rest), Cool-down, and Recovery guidance for each day.
4. Highlight key adjustments made in response to their feedback.
"""

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        models_to_try = ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-2.5-flash"]
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"Update model '{model_name}' failed: {e}")
                continue
    except Exception as e:
        print(f"GenAI Update SDK init failed: {e}")

    try:
        import google.generativeai as genai_legacy
        genai_legacy.configure(api_key=api_key)
        for legacy_model_name in ["gemini-3.5-flash-lite", "gemini-3.8-flash"]:
            try:
                model = genai_legacy.GenerativeModel(legacy_model_name)
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text
            except Exception:
                continue
    except Exception as e:
        print(f"Gemini Update API Exception: {e}")

    return generate_fallback_updated_plan(original_plan, feedback)
