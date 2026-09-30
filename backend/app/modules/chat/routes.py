from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.security import is_authenticated
from app.modules.chat.service import ask_question_service

router = APIRouter()

class AskRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_question(data: AskRequest, user = Depends(is_authenticated)):
    result = ask_question_service(data.question , user)
    return result
