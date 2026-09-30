from fastapi import APIRouter, Depends, UploadFile, File
from app.core.security import is_authenticated
from app.modules.documents.service import upload_pdf_service

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), user = Depends(is_authenticated)):



    result = await upload_pdf_service(file , user.id)
    return result
