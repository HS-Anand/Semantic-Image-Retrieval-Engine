import os

import faiss

faiss.omp_set_num_threads(1)

import numpy as np

from app.indexing.base import IndexBuilder


class FAISSIndexBuilder(IndexBuilder):


    def __init__(self, index_path: str):

        if os.path.exists(index_path):

            print("LOADING EXISTING INDEX")

            self.index = faiss.read_index(index_path)


        else:

            print("CREATING NEW INDEX")

            base_index = faiss.IndexFlatIP(512)

            self.index = faiss.IndexIDMap(base_index)


    def add(self, vector, faiss_id: int):

        embedding = np.array(
            [vector],
            dtype="float32"
        )


        faiss.normalize_L2(embedding)


        ids = np.array(
            [faiss_id],
            dtype="int64"
        )


        self.index.add_with_ids(embedding, ids)


    def save(self, path: str):

        faiss.write_index(
            self.index,
            path
        )