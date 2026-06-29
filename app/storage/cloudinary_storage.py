from typing import List

from concurrent.futures import ThreadPoolExecutor

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


    def upload(self, image_path: str) -> str | None:

        for attempt in range(3):

            try:
                response = cloudinary.uploader.upload(
                    image_path,
                    folder="sire-images"
                )
                return response["secure_url"]

            except Exception:
                print(f"Upload failed ({attempt + 1}/3): {image_path}")

        raise RuntimeError(f"Cloudinary upload failed: {image_path}")


    

    def upload_many(self, image_paths: List[str]) -> List[str]:

        with ThreadPoolExecutor(max_workers=32) as executor:


            urls = list(
                executor.map(
                    self.upload,
                    image_paths
                )
            )


        return urls