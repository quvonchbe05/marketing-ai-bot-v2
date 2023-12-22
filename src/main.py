from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# Routers
from src.chat.routes import router as chat_routes
from src.settings.routes import router as settings_routes
from src.files.routes import router as files_routes
from src.notion.routes import router as notion_router
from src.clear.routes import router as clear_router
from src.auth.routes import router as auth_router
from src.auth.users import router as users_router
from src.history.routes import router as history_router

from src.auth.dependencies import access_route

PROTECTED_ROUTE = Depends(access_route)


app = FastAPI(
    title="Prototype: Marketing Agent Bot",
    version="v0.1",
)

app.include_router(chat_routes)
app.include_router(settings_routes)
app.include_router(history_router)
app.include_router(files_routes)
app.include_router(notion_router)
app.include_router(clear_router)
app.include_router(users_router)
app.include_router(auth_router)

app.mount("/src/uploads/", StaticFiles(directory="src/uploads/"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

