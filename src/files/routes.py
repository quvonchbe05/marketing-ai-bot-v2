from fastapi import APIRouter, UploadFile, HTTPException
from src.db.database import async_session_maker
from src.db.models import FilesModel
from sqlalchemy import insert, select, delete
import os
from typing import List
from pydantic import UUID4
from src.utils.validators import file_upload_validator

router = APIRouter(prefix="/api/files", tags=["File system"])


@router.post("/file/upload")
async def document_upload(files: List[UploadFile]):
    file_paths = []
    validated_files = file_upload_validator(files)
    async with async_session_maker() as session:
        for file in validated_files:
            file_path = f"src/uploads/{file.filename}"

            with open(file_path, "wb") as f:
                f.write(file.file.read())

            stmt = insert(FilesModel).values(file_path=file_path)
            await session.execute(stmt)
            await session.commit()

            file_paths.append(file_path)

    return {"files": file_paths}


@router.get("/list")
async def document_list():
    async with async_session_maker() as session:
        stmt = select(FilesModel)
        response = await session.scalars(stmt)
    return response.all()


@router.delete("/delete/{id}")
async def document_delete(
        id: UUID4,
):
    try:
        async with async_session_maker() as session:
            stmt = select(FilesModel).where(FilesModel.id == id)
            document = await session.scalar(stmt)

            os.remove(document.file_path)

            delete_stmt = delete(FilesModel).where(FilesModel.id == id)
            await session.execute(delete_stmt)
            await session.commit()

        return {"message": "success"}
    except:
        raise HTTPException(status_code=404, detail="File not found!")


@router.delete("/delete/all")
async def document_all_delete():
    async with async_session_maker() as session:
        stmt = select(FilesModel)
        documents = await session.scalars(stmt)
        for document in documents:
            try:
                os.remove(document.file_path)
            except:
                pass

        delete_stmt = delete(FilesModel)
        await session.execute(delete_stmt)
        await session.commit()

    return {"message": "success"}
