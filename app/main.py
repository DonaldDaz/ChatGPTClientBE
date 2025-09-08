from fastapi import FastAPI
from app.routers import chat
from app.routers import kb
from app.routers import ask_kb
from app.routers import diag


def get_app() -> FastAPI:
    app = FastAPI(title="Chat Backend")
    app.include_router(chat.router)
    app.include_router(kb.router)     
    app.include_router(ask_kb.router)
    app.include_router(diag.router)
    return app

app = get_app()
