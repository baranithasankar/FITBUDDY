# FitBuddy – AI Fitness Plan Generator using Gemini Models

FitBuddy is a modern, AI-powered web application built with **FastAPI**, **Jinja2 Templates**, **SQLAlchemy**, **SQLite**, and **Google Gemini AI**. It generates customized 7-day workout plans, personalized nutrition & recovery guidance, and allows users to modify their workout plans using a feedback loop while preserving both original and updated plans in SQLite.

---

## 🚀 Features

- **Personalized 7-Day Workout Generation:** Generates comprehensive daily routines (Warm-up, Main Workout, Sets, Reps/Duration, Rest, Cool-down, Recovery) tailored to user age, weight, goal, and intensity.
- **Fast Nutrition & Recovery Tips:** Uses Gemini Flash models to generate fast, goal-specific nutrition and post-workout guidance.
- **Feedback-Based Plan Updater:** Core interactive feature that updates existing workout routines based on natural language user feedback (e.g. *"Add more cardio"*, *"Include more rest days"*, *"Focus on upper body"*).
- **SQLite Database Persistence:** Stores user profiles, original plans, nutrition tips, user feedback, and updated plans cleanly using SQLAlchemy ORM.
- **Admin All-Users Dashboard:** `/view-all-users` route for inspecting registered users and comparing original vs. updated workout plans.
- **Responsive Dark Fitness Theme:** Modern UI built with glassmorphism, responsive cards, and clean typography.

---

## 🛠️ Project Technology Stack

- **Backend Framework:** FastAPI (Python 3.11+)
- **ASGI Server:** Uvicorn
- **AI Models:** Google Gemini API (`google-genai` & `google-generativeai`)
- **Template Engine:** Jinja2 & HTML5 / CSS3
- **ORM & Database:** SQLAlchemy & SQLite
- **Validation:** Pydantic
- **Form Parsing:** python-multipart
- **Environment Management:** python-dotenv

---

## 📁 Required Project Structure

```text
FitBuddy/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── gemini_generator.py
│   ├── gemini_flash_generator.py
│   └── updated_plan.py
│
├── templates/
│   ├── index.html
│   ├── result.html
│   └── all_users.html
│
├── static/
│   ├── style.css
│   └── images/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation Instructions

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Create Virtual Environment
```bash
# On Windows (PowerShell / Command Prompt)
py -3.11 -m venv venv

# Activate Virtual Environment (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate Virtual Environment (Command Prompt)
.\venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (`.env`)
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
```
> **Note:** Replace `your_api_key_here` with a valid Google Gemini API Key. If no key is provided, the application runs in a graceful demo mode with structured templates.

---

## 🏃 Running the Application

Start the FastAPI application using Uvicorn:

```bash
python -m app.main
# or
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

---

## 🌐 URLs & Endpoints

- **Main Homepage:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive API Docs (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Admin Dashboard:** [http://127.0.0.1:8000/view-all-users](http://127.0.0.1:8000/view-all-users)

---

## 🛣️ Main Application Routes

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Displays the homepage with user input form |
| `POST` | `/generate-workout` | Validates input, calls Gemini, stores profile & original plan in SQLite, renders result |
| `POST` | `/submit-feedback` | Retrieves original plan, sends feedback to Gemini, generates and stores updated plan separately |
| `GET` | `/view-all-users` | Renders admin view table listing all registered users and their plans |

---

## 🤖 How Gemini AI is Used

1. **`app/gemini_generator.py` (`generate_workout_gemini`):** Structured prompt generating 7-day day-by-day workout routines with warm-ups, exercises, sets, reps, rest, cool-down, and daily recovery.
2. **`app/gemini_flash_generator.py` (`generate_nutrition_tip_with_flash`):** Lightweight Gemini model generating goal-specific macro advice, hydration goals, post-workout window guidance, and sleep targets.
3. **`app/updated_plan.py` (`update_workout_plan`):** Context-aware prompt receiving the user's original plan + feedback to generate a revised plan while keeping the original intact in the database.

---

## 📄 License
Project created for **Naan Mudhalvan**.
