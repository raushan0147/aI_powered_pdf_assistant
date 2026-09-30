import os
import shutil
from fastapi import UploadFile

from app.modules.rag.loader import load_pdf
from app.modules.rag.splitter import split_documents
from app.modules.rag.vectorstore import store_documents

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def upload_pdf_service(file: UploadFile, user_id: int):
    user_folder = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    # Delete only this user's old PDF file
    for old_file in os.listdir(user_folder):
        old_file_path = os.path.join(user_folder, old_file)

        if os.path.isfile(old_file_path):
            os.remove(old_file_path)

    # Save new PDF
    new_file_path = os.path.join(user_folder, file.filename)

    with open(new_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Load PDF
    docs = load_pdf(new_file_path)

    # Split PDF
    splitted_docs = split_documents(docs)

    # Store embeddings with user_id metadata
    result = store_documents(
        splitted_docs=splitted_docs,
        user_id=user_id,
        filename=file.filename
    )

    return {
        "message": "Old user PDF and embeddings replaced successfully",
        "user_id": user_id,
        "filename": file.filename,
        "path": new_file_path,
        "chunks": len(splitted_docs),
        "vector_result": result
    }