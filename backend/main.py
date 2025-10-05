from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from colorthief import ColorThief
import io
import uuid

# supbase imports for database handling
from supabase import create_client
import os

app = FastAPI()

# -------------------
# CORS (for React frontend)
# -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# supabase setup

# project url
SUPABASE_URL = "https://plwnpokeijdctfobhrwq.supabase.co"
# anon key
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBsd25wb2tlaWpkY3Rmb2JocndxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2MDUxOTAsImV4cCI6MjA3NTE4MTE5MH0.omfImjVI86EM91hmhYDk42vo_n1U6z18ffCSF3q8c0g"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------
# Routes
# -------------------
@app.get("/")
def home():
    return {"message": "FitForecast backend is running!"}

# the following code allows user to upload their image,
# then, the file is stored, and meta data is extracted
@app.post("/upload")
async def upload_garment(
    file: UploadFile = File(...),
    garment_type: str = Form(...)
):
    # 1. Read file bytes
    file_bytes = await file.read()
    
    # 2. Generate unique filename
    file_ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    
    # 3. Upload file to Supabase Storage
    res = supabase.storage.from_("garments").upload(unique_filename, file_bytes)
    if res.get("error"):
        return {"error": res["error"]["message"]}
    
    # 4. Get public URL
    file_url = supabase.storage.from_("garments").get_public_url(unique_filename).get("publicUrl")
    
    # 5. Extract color palette
    color_thief = ColorThief(io.BytesIO(file_bytes))
    palette = color_thief.get_palette(color_count=5)
    palette_hex = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in palette]
    
    # 6. tags (based on type) AI should assign these
    tags = ["summer"] if garment_type.lower() in ["skirt","top"] else ["winter"]
    
    # 7. Insert into Supabase bucket "garments"
    supabase.table("garments").insert({
        "filename": unique_filename,
        "file_url": file_url,
        "garment_type": garment_type,
        "color_palette": palette_hex,
        "tags": tags
    }).execute()
    
    # 8. Return metadata
    return {
        "filename": unique_filename,
        "file_url": file_url,
        "garment_type": garment_type,
        "color_palette": palette_hex,
        "tags": tags
    }