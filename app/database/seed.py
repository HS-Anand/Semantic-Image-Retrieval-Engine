from app.database.session import SessionLocal
from app.database.models import ImageAsset


def seed_data():

    db = SessionLocal()

    image = ImageAsset(
        file_name="test_image.jpg",
        image_url="https://example.com/test.jpg",
        quality_score=0.9,
        index_status="INDEXED"
    )

    db.add(image)

    db.commit()

    print(image.id)

    db.close()


if __name__ == "__main__":

    seed_data()