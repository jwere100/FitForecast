from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FitForecast backend is running!"}

@app.post("/upload")
async def upload_garment(file: UploadFile):
    return {"filename": file.filename}

# CORS
app = FastAPI()

# Allow React frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_garment(file: UploadFile = File(...)):
    return {"filename": file.filename}
