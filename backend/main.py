from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from PIL import Image
import shutil
import sys

# Add DeepFashion2 API folder to path
sys.path.append(str(Path(__file__).parent / "utils/deepfashion2_api"))
from wardrobe import extract_attributes, save_uploaded_image
from utils.deepfashion2_api import deepfashion2_utils

# Optional: if using a background removal library
# pip install rembg
from rembg import remove

app = FastAPI()

# CORS for your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder to store uploads
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        #save file
        saved_path = await save_uploaded_image(file, upload_dir=UPLOAD_FOLDER)
        
        #Remove the background to make wardrobe cleaner
        input_image = Image.open(saved_path).convert("RGBA")
        output_image = remove(input_image)
        output_path = UPLOAD_FOLDER / f"processed_{file.filename}"
        output_image.save(output_path)

        #Extract data from deepfashion
        metadata = extract_attributes(str(output_path))

        #Return data
        return {
            "filename": file.filename,
            "processed_image": str(output_path),
            "metadata": metadata
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
def home():
    return {"message": "FitForecast backend is running!"}

@app.get("/uploads/{filename}")
def get_image(filename: str):
    """
    Serve uploaded or processed images
    """
    file_path = UPLOAD_FOLDER / filename
    if file_path.exists():
        return FileResponse(file_path)
    return JSONResponse(content={"error": "File not found"}, status_code=404)