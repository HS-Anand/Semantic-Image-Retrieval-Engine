import os

import faiss

from app.database.session import SessionLocal
from app.database.models import ImageAsset

import cloudinary
import cloudinary.api

from app.config import settings



def reset_database(db):

    print("Deleting database rows")

    db.query(
        ImageAsset
    ).delete()

    db.commit()

    print("Database cleared")



def reset_faiss():

    print("Deleting FAISS index")


    index_path = "storage/image.index"


    if os.path.exists(
        index_path
    ):

        os.remove(
            index_path
        )


    # create empty index again

    base_index = (
        faiss.IndexFlatIP(
            512
        )
    )

    index = (
        faiss.IndexIDMap(
            base_index
        )
    )


    faiss.write_index(
        index,
        index_path
    )


    print("FAISS reset")



def reset_cloudinary():

    print("Deleting Cloudinary images")


    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET
    )


    result = (
        cloudinary.api
        .delete_resources_by_prefix(
            "sire-images/"
        )
    )


    cloudinary.api.delete_folder(
        "sire-images"
    )


    print(result)

    print("Cloudinary cleared")



if __name__ == "__main__":


    db = SessionLocal()


    try:

        reset_cloudinary()

        reset_faiss()

        reset_database(db)


        print(
            "SIRE storage reset complete"
        )


    finally:

        db.close()