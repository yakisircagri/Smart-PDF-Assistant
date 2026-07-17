from fastapi import APIRouter, UploadFile, File

from services.upload_service import upload_pdf


router=APIRouter()


@router.post("/upload")
async def upload(
    file:UploadFile=File(...)
):

    return await upload_pdf(file)