from app.database.models import ImageAsset


class ImageRepository:

    def __init__(self, db):

        self.db = db


    def get_ranking_features(self, image_ids):

        return (
            self.db
            .query(
                ImageAsset.id,
                ImageAsset.quality_score
            )
            .filter(
                ImageAsset.id.in_(image_ids)
            )
            .all()
        )


    def hydrate_results(self, image_ids):

        results =  (
            self.db
            .query(
                ImageAsset.id,
                ImageAsset.file_name,
                ImageAsset.image_url
            )
            .filter(
                ImageAsset.id.in_(image_ids)
            )
            .all()
        )
    
        return [
            {
                "id": str(result.id),
                "file_name": result.file_name,
                "image_url": result.image_url
            }
            for result in results
        ]