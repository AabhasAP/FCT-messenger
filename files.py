from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
import boto3
from botocore.client import Config
import uuid
from app.core.config import settings
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

# Initialize S3 client
s3_client = boto3.client(
    's3',
    endpoint_url=settings.S3_ENDPOINT,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    region_name=settings.S3_REGION
)

class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    file_type: str
    file_size: int
    url: str

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload a file to S3."""
    # Validate file type
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Read file
    contents = await file.read()
    file_size = len(contents)
    
    # Validate file size
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Generate unique file ID
    file_id = str(uuid.uuid4())
    file_key = f"{current_user.id}/{file_id}/{file.filename}"
    
    # Upload to S3
    try:
        s3_client.put_object(
            Bucket=settings.S3_BUCKET,
            Key=file_key,
            Body=contents,
            ContentType=file.content_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    # Generate URL
    url = f"{settings.S3_ENDPOINT}/{settings.S3_BUCKET}/{file_key}"
    
    return FileUploadResponse(
        file_id=file_id,
        filename=file.filename,
        file_type=file.content_type,
        file_size=file_size,
        url=url
    )

@router.get("/{file_id}/download")
async def download_file(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Generate a presigned URL for file download."""
    # In production, look up file metadata from database
    file_key = f"{current_user.id}/{file_id}/filename.ext"
    
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.S3_BUCKET, 'Key': file_key},
            ExpiresIn=3600
        )
        return {"download_url": url}
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")
