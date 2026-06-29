
from app.database.models import ImageAsset
from sqlalchemy import func

class ImageRepository:

    def __init__(self, db):

        self.db = db

    def exists_by_file_name(self, file_name):

        return (
            self.db.query(ImageAsset).filter(
                ImageAsset.file_name == file_name
            ).first() is not None
        )


    def get_next_faiss_id(self):

        max_id = (
            self.db.query(
                func.max(ImageAsset.faiss_id)
            ).scalar()
        )

        if max_id is None:
            return 0

        return max_id + 1

    def get_ranking_features(self, faiss_ids):

        return (
            self.db
            .query(
                ImageAsset.faiss_id,
                ImageAsset.quality_score
            )
            .filter(
                ImageAsset.faiss_id.in_(faiss_ids)
            )
            .all()
        )


    def hydrate_results(self, faiss_ids):

        results = (
            self.db
            .query(
                ImageAsset.id,
                ImageAsset.faiss_id,
                ImageAsset.file_name,
                ImageAsset.image_url
            )
            .filter(
                ImageAsset.faiss_id.in_(faiss_ids)
            )
            .all()
        )


        return [
            {
                "id": str(result.id),
                "faiss_id": result.faiss_id,
                "file_name": result.file_name,
                "image_url": result.image_url
            }

            for result in results
        ]

    def create(
        self,
        faiss_id: int,
        file_name: str,
        image_url: str,
        quality_score: float,
        category: str = None
    ):

        image = ImageAsset(
            faiss_id=faiss_id,
            file_name=file_name,
            image_url=image_url,
            quality_score=quality_score,
            category=category,
            index_status="INDEXED"
        )


        self.db.add(image)

        self.db.commit()

        self.db.refresh(image)


        return image 
    

    def create_many(self, images_data):

        try:

            images = [
                ImageAsset(
                    faiss_id=data["faiss_id"],
                    file_name=data["file_name"],
                    image_url=data["image_url"],
                    quality_score=data["quality_score"],
                    category=data.get("category"),
                    index_status="INDEXED"
                )
                for data in images_data
            ]

            self.db.add_all(images)
            self.db.commit()

            return images
        
        except Exception:
            self.db.rollback()
            raise