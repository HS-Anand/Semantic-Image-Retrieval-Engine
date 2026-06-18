from abc import ABC, abstractmethod
from typing import List, Tuple


class VectorStore(ABC):

    @abstractmethod
    def search(self, vector: List[float], k: int) -> List[Tuple[int, float]]:
        pass