from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import documents, export, health, notes, sessions, settings, skills
from core.config import settings as app_settings
from core.logging import setup_logging
from db.engine import init_db

setup_logging()
init_db()

app = FastAPI(title=app_settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api = FastAPI()
api.include_router(health.router)
api.include_router(documents.router)
api.include_router(skills.router)
api.include_router(notes.router)
api.include_router(sessions.router)
api.include_router(settings.router)
api.include_router(export.router)
app.mount("/api", api)
