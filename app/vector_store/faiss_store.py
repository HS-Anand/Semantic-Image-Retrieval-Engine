from typing import List, Tuple

import faiss
import numpy as np

faiss.omp_set_num_threads(1)

from app.vector_store.base import VectorStore


MIN_SIMILARITY = 0.22
RELATIVE_MARGIN = 0.12


class FAISSVectorStore(VectorStore):

    def __init__(
        self,
        index_path: str
    ):

        self.index = faiss.read_index(
            index_path
        )


    def search(
        self,
        vector: List[float],
        k: int
    ) -> List[Tuple[int, float]]:


        query_vector = np.array(
            [vector],
            dtype="float32"
        )


        faiss.normalize_L2(
            query_vector
        )


        scores, ids = (
            self.index.search(
                query_vector,
                k
            )
        )


        results = []


        if len(scores[0]) == 0:

            return results



        best_score = scores[0][0]


        threshold = max(
            MIN_SIMILARITY,
            best_score - RELATIVE_MARGIN
        )


        print(
            "Similarity threshold:",
            threshold
        )


        for image_id, score in zip(
            ids[0],
            scores[0]
        ):

            print(
                image_id,
                score
            )


            if image_id == -1:
                continue


            if score < threshold:
                continue


            results.append(
                (
                    int(image_id),
                    float(score)
                )
            )


        return results