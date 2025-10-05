from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Query
import requests

# Initialize FastAPI
app = FastAPI()

# ---- Routes ----
@app.get("/")
def home():
    return {"message": "FitForecast backend is running!"}

@app.post("/upload")
async def upload_garment(file: UploadFile):
    return {"filename": file.filename}

# ---- CORS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Weather Endpoint ----
@app.get("/weather")
def get_weather(city: str = Query(..., description="City name")):
    api_key = "c124e5a731e3c59d81bffb262eb02c00"  # replace with your OpenWeatherMap key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if "main" not in data:
        return {"error": "City not found", "details": data}

    temp = data["main"]["temp"]
    condition = data["weather"][0]["description"] if "weather" in data else ""

    # Simple clothing logic
    if temp < 5:
        recommendation = "Wear a heavy coat, scarf, and gloves 🧥🧣🧤"
    elif temp < 15:
        recommendation = "A sweater or light jacket should be fine 🧥"
    elif temp < 25:
        recommendation = "T-shirt and jeans are perfect 👕👖"
    else:
        recommendation = "It’s hot! Wear shorts and stay cool 🩳😎"

    # Add condition-specific recommendations
    if "rain" in condition.lower():
        recommendation += " 🌧️ Don’t forget an umbrella!"
    if "snow" in condition.lower():
        recommendation += " ❄️ Wear boots and gloves."
    if "wind" in condition.lower():
        recommendation += " 💨 A windbreaker will help."

    return {
        "city": city,
        "temperature": temp,
        "weather": condition,
        "recommendation": recommendation
    }
