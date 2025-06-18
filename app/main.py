from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import analyze  # asegúrate de tener analyze.py

app = FastAPI()

# Permitir conexión desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyze.process_audio(contents)
    return result
