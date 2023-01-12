from fastapi import FastAPI, UploadFile
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, Response
from files import s3, upload_file, download_file
from settings import AWS_S3_BUCKET_NAME

app = FastAPI()


@app.put("/{key}")
def create_or_update_file(key: str, file: UploadFile):
    if upload_obj := upload_file(s3(), file, AWS_S3_BUCKET_NAME, key):
        return JSONResponse(content="Object has been uploaded successfully",
                            status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="File could not be uploaded")


@app.get("/{key}")
def get_file(key: str):
    if download_obj := download_file(s3(), key, AWS_S3_BUCKET_NAME):
        return Response(content=download_obj['content'], media_type=download_obj['media_type'],
                        status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="There is no such a key")
