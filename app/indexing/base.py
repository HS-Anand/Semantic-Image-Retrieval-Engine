from abc import ABC, abstractmethod
from typing import List


class IndexBuilder(ABC):


    @abstractmethod
    def add(self, vector: List[float], item_id: int):
        pass

    @abstractmethod
    def add_many(self, vectors: List[List[float]], item_ids: List[int]):
        pass

    @abstractmethod
    def save(self, path: str):
        pass