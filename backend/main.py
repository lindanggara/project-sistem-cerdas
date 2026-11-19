import os
import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.predictor import Predictor
from services.topic_model import TopicModel
from services.anonymizer import Anonymizer
from services.preprocessor import preprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("textscope")

state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading model & services...")
    state["predictor"] = Predictor(model_path=os.getenv("MODEL_PATH", "models/logreg_tuned.pkl"))
    state["topic_model"] = TopicModel(n_topics=int(os.getenv("N_TOPICS", "5")))
    state["anonymizer"] = Anonymizer()
    logger.info("Model & services loaded.")
    yield
    state.clear()
    logger.info("Shutdown.")


app = FastAPI(
    title="TextScope API",
    description="Analisis teks: klasifikasi emosi, topic modeling, anonimisasi.",
    version="1.0.0",
    lifespan=lifespan,
)

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    label: str
    confidence: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Teks kosong.")
    text_clean = preprocess(req.text)
    text_anon = state["anonymizer"].anonymize(text_clean)
    label, confidence = state["predictor"].predict(text_anon)
    return PredictResponse(label=label, confidence=confidence)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    filename = file.filename or ""
    if not (filename.endswith(".csv") or filename.endswith(".xlsx")):
        raise HTTPException(status_code=400, detail="File harus .csv atau .xlsx")

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file, engine="openpyxl")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Gagal membaca file: {e}")

    if df.empty:
        raise HTTPException(status_code=400, detail="File kosong.")

    MAX_ROWS = int(os.getenv("MAX_ROWS", "5000"))
    if len(df) > MAX_ROWS:
        raise HTTPException(
            status_code=400,
            detail=f"Maksimal {MAX_ROWS} baris. File kamu: {len(df)} baris.",
        )

    text_col = df.columns[0]
    texts = df[text_col].astype(str).tolist()

    cleaned = [preprocess(t) for t in texts]
    anon = [state["anonymizer"].anonymize(t) for t in cleaned]
    predictions = state["predictor"].predict_batch(anon)

    topics = state["topic_model"].fit_transform(anon[:2000])

    label_counts = pd.Series([p["label"] for p in predictions]).value_counts().to_dict()

    return {
        "total_rows": len(df),
        "text_column": text_col,
        "label_distribution": label_counts,
        "predictions": predictions[:50],
        "topics": topics,
        "preview_anonymized": [
            {"original": texts[i], "anonymized": anon[i]}
            for i in range(min(10, len(texts)))
        ],
    }
