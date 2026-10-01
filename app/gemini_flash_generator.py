import os
from dotenv import load_dotenv

load_dotenv()

def generate_fallback_nutrition_tip(goal: str, intensity: str, age: int, weight: float) -> str:
    """Fallback nutrition generator when Gemini API Key is missing or invalid."""
    daily_protein = round(weight * 1.6, 1)
    daily_water = round(weight * 0.04, 1)
    return f"""🥗 **Nutrition & Recovery Tip for {goal} ({intensity} Intensity)**

* **Protein Optimization:** Aim for approximately **{daily_protein}g of high-quality protein** daily (lean chicken, fish, eggs, tofu, or whey) split across 4 meals to maximize muscle recovery.
* **Hydration Goal:** Drink at least **{daily_water} Liters of water daily**, increasing by 500ml on workout days to maintain cellular performance.
* **Post-Workout Window:** Consume a 3:1 ratio of carbs to protein within 45 minutes after intense workouts to replenish glycogen stores.
* **Recovery Protocol:** Prioritize 7.5 to 8.5 hours of uninterrupted sleep every night for optimal growth hormone secretion and tissue repair.
"""

def generate_nutrition_tip_with_flash(goal: str, intensity: str, age: int, weight: float) -> str:
    """Generate concise nutrition and recovery tip using Gemini Flash fast model."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key or api_key == "your_api_key_here":
        return generate_fallback_nutrition_tip(goal, intensity, age, weight)

    prompt = f"""
You are FitBuddy's nutrition and recovery expert AI.
Provide a concise, high-impact nutrition and recovery tip for a user with the following profile:

- Age: {age} years
- Weight: {weight} kg
- Fitness Goal: {goal}
- Workout Intensity: {intensity}

Include guidance on:
1. Daily protein & macro targets tailored to their weight ({weight} kg) and goal ({goal})
2. Hydration advice
3. Post-workout nutrition timing
4. Sleep & recovery protocol

Keep the tip concise, actionable, and formatted nicely with bullet points and bold headers.
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
                print(f"Flash model '{model_name}' failed: {e}")
                continue
    except Exception as e:
        print(f"GenAI Flash SDK init failed: {e}")

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
        print(f"Gemini Flash API Exception: {e}")

    return generate_fallback_nutrition_tip(goal, intensity, age, weight)
