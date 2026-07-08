import os, cloudinary, cloudinary.api, cloudinary.uploader
from fastapi import APIRouter, UploadFile, File, Form
from dotenv import load_dotenv

router = APIRouter(prefix="/api/v1/cloudinary", tags=["Cloudinary"])

load_dotenv()
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# Upload file data to cloud storage
@router.post("/upload")
async def upload_to_cloud(
    file: UploadFile=File(...), # File data from request body
    folder: str=Form(...), # Get folder name from request body
    upload_preset: str=Form(...) # Get the upload_preset from request body
):
    try:
        # Upload file to cloudinary storage
        response = cloudinary.uploader.upload(
            file.file,
            folder=folder,
            upload_preset=upload_preset,
            filename_override=file.filename,
            use_filename=True,
            unique_filename=True
        )

        return {
            "status": "Success",
            "file_name": file.filename,
            "public_id": response["public_id"],
            "secure_url": response["secure_url"]
        }

    except Exception as e:
        return { "status": "Error", "message": str(e) }
    
# Delete images as article is deleted
@router.post("/delete")
async def delete_images(public_ids: list):
    try:
        response = cloudinary.api.delete_resources(public_ids, invalidate=True)
        print(response)

    except Exception as e:
        return { "status": "Error", "message": str(e) }