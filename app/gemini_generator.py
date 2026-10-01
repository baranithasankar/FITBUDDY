import os
from dotenv import load_dotenv

load_dotenv()

def generate_fallback_workout_plan(username: str, age: int, weight: float, goal: str, intensity: str) -> str:
    """Fallback generator when Gemini API Key is missing or invalid."""
    return f"""### 🏋️ Personalized 7-Day Workout Plan for {username} (Demo Mode)

> **Note:** `GEMINI_API_KEY` is missing or invalid in `.env`. Displaying structured demo fitness plan for **{goal}** at **{intensity}** intensity.

---

### **Day 1: Upper Body & Core Strength**
* **Focus:** Chest, Shoulders, Triceps, Abs
* **Warm-up (7 mins):** Dynamic arm circles, light jumping jacks, torso twists (2 sets)
* **Main Workout:**
  * Push-ups / Knee Push-ups: 3 sets x 10-12 reps (Rest: 60s)
  * Dumbbell / Water Bottle Overhead Press: 3 sets x 12 reps (Rest: 60s)
  * Plank Hold: 3 sets x 30-45 seconds (Rest: 45s)
* **Cool-down (5 mins):** Chest opening stretch, shoulder stretches
* **Recovery Guidance:** Hydrate well with at least 3L of water today.

---

### **Day 2: Lower Body Power & Mobility**
* **Focus:** Quads, Hamstrings, Glutes, Calves
* **Warm-up (8 mins):** Bodyweight squats, leg swings, ankle rotations
* **Main Workout:**
  * Bodyweight Squats: 4 sets x 15 reps (Rest: 60s)
  * Walking Lunges: 3 sets x 12 reps per leg (Rest: 60s)
  * Glute Bridges: 3 sets x 15 reps (Rest: 45s)
* **Cool-down (5 mins):** Hamstring & Quad static stretches
* **Recovery Guidance:** Ensure adequate protein intake after workout.

---

### **Day 3: Active Recovery & Mobility**
* **Focus:** Full body flexibility and core stability
* **Warm-up (5 mins):** Cat-cow stretch, child's pose
* **Main Workout:**
  * 30-minute brisk walk or light cycling
  * Yoga stretch routine: 15 minutes
* **Cool-down (5 mins):** Deep breathing exercises
* **Recovery Guidance:** Get 7-8 hours of restful sleep.

---

### **Day 4: Back & Biceps Focus**
* **Focus:** Upper back, Latissimus, Biceps
* **Warm-up (7 mins):** Arm swings, scapular retractions
* **Main Workout:**
  * Resistance Band or Towel Rows: 4 sets x 12 reps (Rest: 60s)
  * Bicep Curls: 3 sets x 12-15 reps (Rest: 45s)
  * Superman Hold: 3 sets x 30 seconds (Rest: 45s)
* **Cool-down (5 mins):** Cobra stretch & Upper back stretch
* **Recovery Guidance:** Consume complex carbs post-workout.

---

### **Day 5: Full Body High Intensity & Cardio**
* **Focus:** Cardiovascular endurance & fat burn
* **Warm-up (8 mins):** Jogging in place, high knees
* **Main Workout:**
  * Mountain Climbers: 4 sets x 30 seconds (Rest: 30s)
  * Burpees / Modified Burpees: 3 sets x 10 reps (Rest: 60s)
  * Jumping Jacks: 4 sets x 45 seconds (Rest: 30s)
* **Cool-down (5 mins):** Full body static stretch
* **Recovery Guidance:** Replenish electrolytes after high sweating.

---

### **Day 6: Core & Balance Training**
* **Focus:** Abdominals, Obliques, Lower Back
* **Warm-up (5 mins):** Torso rotations, hip circles
* **Main Workout:**
  * Bicycle Crunches: 3 sets x 20 reps (Rest: 45s)
  * Side Planks: 3 sets x 25 seconds per side (Rest: 45s)
  * Bird-Dog Exercise: 3 sets x 12 reps per side (Rest: 45s)
* **Cool-down (5 mins):** Child's pose & abdominal stretch
* **Recovery Guidance:** Take a warm shower to relax muscles.

---

### **Day 7: Full Rest & Regeneration**
* **Focus:** Complete muscle recovery
* **Activities:** Light stretching, leisurely walk, mental relaxation
* **Recovery Guidance:** Plan meals for the upcoming week and focus on hydration.
"""

def generate_workout_gemini(username: str, user_id: str, age: int, weight: float, goal: str, intensity: str) -> str:
    """Generate a 7-day personalized workout plan using Gemini AI."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key or api_key == "your_api_key_here":
        return generate_fallback_workout_plan(username, age, weight, goal, intensity)

    prompt = f"""
You are FitBuddy, an elite personal AI fitness trainer.
Generate a structured, highly personalized 7-day workout plan for this user:

- User Name: {username}
- User ID: {user_id}
- Age: {age} years old
- Weight: {weight} kg
- Fitness Goal: {goal}
- Workout Intensity Level: {intensity}

Formatting & Content Requirements:
1. Provide a clear title with the user's name and goal.
2. Provide details for Day 1 through Day 7 in order.
3. For each day, include:
   - Day Title & Focus Area
   - Warm-up Routine (duration & exercises)
   - Main Workout (exercises, sets, reps or duration, rest intervals)
   - Cool-down Routine
   - Recovery Guidance
4. Use clean Markdown headings (### Day 1: ...), bold text, bullet points, and tables where applicable.
5. Tailor exercise choices and rest periods specifically for a {age}-year-old individual weighing {weight} kg pursuing {goal} at {intensity} intensity.
"""

    # Try calling Google GenAI / GenerativeAI SDK
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        # Try currently supported Gemini models
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
                print(f"GenAI model '{model_name}' failed: {e}")
                continue
    except Exception as e:
        print(f"GenAI SDK init failed: {e}")

    try:
        # Try legacy google.generativeai SDK as fallback
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
        print(f"Gemini API Exception: {e}")

    # If API call fails (e.g. quota limit, invalid key), return fallback plan
    return generate_fallback_workout_plan(username, age, weight, goal, intensity)
