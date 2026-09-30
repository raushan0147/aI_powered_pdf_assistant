from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.chat.routes import router as chat_router
from app.modules.documents.routes import router as doc_router
from app.modules.users.routes import router as user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1):\d+$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(doc_router, prefix="/api/documents")
app.include_router(chat_router, prefix="/api/chat")
app.include_router(user_router)
