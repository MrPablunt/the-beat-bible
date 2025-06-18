from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import essentia
import essentia.standard as es

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open("temp.wav", "wb") as f:
            f.write(contents)

        loader = es.MonoLoader(filename="temp.wav")
        audio = loader()

        bpm = es.RhythmExtractor2013(method="multifeature")(audio)[0]
        key, scale, strength = es.KeyExtractor()(audio)

        return {
            "bpm": round(bpm),
            "key": key,
            "scale": scale,
            "genre": "Desconocido",
            "mood": "Indefinido"
        }

    except Exception as e:
        return {"error": str(e)}