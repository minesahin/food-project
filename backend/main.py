from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid

from model import detect_foods
from nutrition import get_nutrition_list
from rules import check_suitability

app = FastAPI(
    title="Tabak Uygunluk API",
    description="Hastaliga gore tabak icerigi uygunluk tespit sistemi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"mesaj": "Tabak Uygunluk API calisiyor", "versiyon": "1.0.0"}


@app.get("/health")
def health():
    return {"durum": "aktif"}


@app.post("/analyze")
async def analyze(
    image: UploadFile = File(...),
    disease: str = Form(...)
):
    file_ext = image.filename.split(".")[-1] if "." in image.filename else "jpg"
    file_name = str(uuid.uuid4()) + "." + file_ext
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(image.file, f)

    try:

        detected = detect_foods(file_path)
        food_labels = list(set([d["label"] for d in detected]))

        nutrition = get_nutrition_list(food_labels)

        suitability = check_suitability(food_labels, disease)

        return {
            "basarili": True,
            "tespit": detected,
            "besin_degerleri": nutrition,
            "uygunluk": suitability
        }

    except Exception as e:
        return {
            "basarili": False,
            "hata": str(e)
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@app.get("/diseases")
def get_diseases():
    return {
        "desteklenen_hastaliklar": [
            "diyabet",
            "hipertansiyon",
            "obezite",
            "bobrek"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
