import uuid

from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from sqlalchemy import Integer

from app.database.session import Base


class ImageAsset(Base):

    __tablename__ = "images"


    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    faiss_id = Column(
        Integer,
        unique=True,
        index=True
    )


    file_name = Column(
        String,
        nullable=False
    )


    category = Column(
        String
    )


    image_url = Column(
        String,
        nullable=False
    )


    quality_score = Column(
        Float,
        default=1.0
    )


    index_status = Column(
        String,
        default="UPLOADED"
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )