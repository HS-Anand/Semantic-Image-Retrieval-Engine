from abc import ABC, abstractmethod


class ImageStorage(ABC):


    @abstractmethod
    def upload(self, image_path: str) -> str:
        pass