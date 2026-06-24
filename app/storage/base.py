from abc import ABC, abstractmethod
from typing import List


class ImageStorage(ABC):


    @abstractmethod
    def upload(self, image_path: str) -> str:
        pass

    @abstractmethod
    def upload_many(self, image_paths: List[str]) -> List[str]:
        pass