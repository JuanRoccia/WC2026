import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.web.routes import router

app = FastAPI(
    title="WC2026 Predictor",
    description="Sistema de predicción de resultados para el Mundial FIFA 2026",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


def start():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8001, reload=True)


if __name__ == "__main__":
    start()
