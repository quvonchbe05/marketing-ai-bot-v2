from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Routers
from src.chat.routes import router as chat_routes
from src.settings.routes import router as settings_routes
from src.files.routes import router as files_routes
from src.notion.routes import router as notion_router
from src.clear.routes import router as clear_router


app = FastAPI(
    title="Prototype: Marketing Agent Bot",
    version="v0.1",
)

app.include_router(chat_routes)
app.include_router(settings_routes)
app.include_router(files_routes)
app.include_router(notion_router)
app.include_router(clear_router)

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



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        port=8000,
        host="0.0.0.0",
        reload=True,
    )
