# src/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router

app = FastAPI(
    title="Doc to Markup Converter",
    description="Converts printed documents to Markdown using OCR and layout detection.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)        # ← removed prefix="/api"

@app.get("/")
async def root():
    return {"message": "Doc to Markup API is running"}

@app.get("/health")
async def health():
    return {"status": "ok"}