import cloudinary
import cloudinary.uploader

from app.config import settings
from app.storage.base import ImageStorage


class CloudinaryStorage(ImageStorage):


    def __init__(self):

        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )


    def upload(self, image_path: str) -> str:


        response = cloudinary.uploader.upload(
            image_path,
            folder="sire-images"
        )


        return response["secure_url"]