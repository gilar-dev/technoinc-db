import os, cloudinary, cloudinary.api, cloudinary.uploader
from fastapi import APIRouter, UploadFile, File, Form
from dotenv import load_dotenv
from configuration.model import ImagePublicId, ImageFormData
from typing import Optional, List

router = APIRouter(prefix="/api/v1/cloudinary", tags=["Cloudinary"])

load_dotenv()
cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure = True
)

# Upload file data to cloud storage
@router.post("/upload")
async def upload_to_cloud(
    file: List[UploadFile] = File(...), # Get file data from request body
    folder: str = Form(...), # Get folder name from request body
    upload_preset: str = Form(...) # Get the upload_preset from request body
):
    try:
        public_ids: List[str] = []
        secure_urls: List[str] = []
        for item in file:
            # Upload file to cloudinary storage
            response: dict = cloudinary.uploader.upload(
                item.file,
                folder = folder,
                upload_preset = upload_preset,
                filename_override = item.filename,
                use_filename = True,
                unique_filename = True
            )
            public_ids.append(response.get("public_id"))
            secure_urls.append(response.get("secure_url"))
        return {
            "status": "Success",
            "public_ids": public_ids,
            "secure_urls": secure_urls
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }
    
# Delete images as article is deleted
@router.delete("/delete")
async def delete_images(data: ImagePublicId, folder: Optional[str]):
    try:
        # Get list of public ids
        loaded_data = data.model_dump()
        public_ids = loaded_data.get("public_ids")
        # Delete asset by using Upload API destroy method
        for pid in public_ids:
            cloudinary.uploader.destroy(pid, invalidate=True)
        # Delete folder in cloudinary (optional)
        if folder == "yes":
            cloudinary.api.delete_folder(loaded_data.get("folder_name"))
        return {
            "status": "Success",
            "message": "Deleted"
        }
    except Exception as e:
        return { "status": "Error", "message": str(e) }