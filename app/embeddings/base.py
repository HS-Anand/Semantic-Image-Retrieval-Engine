from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):

    @abstractmethod
    def encode_text(self, text: str) -> List[float]:
        pass


    @abstractmethod
    def encode_image(self, image_path: str) -> List[float]:
        pass