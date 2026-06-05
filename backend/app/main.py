from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.chat import router as chat_router
from .api.calculator import router as calculator_router
from .api.documents import router as documents_router
from .api.memory import router as memory_router
from .api.training import router as training_router

app = FastAPI(
    title="KAYA API",
    description="Local API for the KAYA AI workspace.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "kaya-api"}


app.include_router(chat_router, prefix="/api")
app.include_router(calculator_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
app.include_router(memory_router, prefix="/api")
app.include_router(training_router, prefix="/api")
