from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import RedirectResponse
from starlette import status

from .dependencies import is_valid_filename
from .api import S3Worker

from .exceptions import TooLargeFile

import uuid

s3_router = APIRouter()


@s3_router.on_event("startup")
async def startup():
    await S3Worker.new_bucket("avatars", True)


@s3_router.post("/upload_file", status_code=status.HTTP_200_OK)
async def upload_file(file: UploadFile):
    id = str(uuid.uuid4())

    if file.size > 30 * 1024 * 1024:
        raise TooLargeFile(file.size)

    return {
        "filename": id,
        "url": await S3Worker.upload_file("avatars", file, filename=id)
    }


@s3_router.get("/file/{filename:path}", status_code=status.HTTP_200_OK)
async def get_file_url(filename: str = Depends(is_valid_filename), redirect: bool = False):
    url = await S3Worker.get_file_url("avatars", filename)

    return RedirectResponse(url, status_code=status.HTTP_302_FOUND) if redirect else url
