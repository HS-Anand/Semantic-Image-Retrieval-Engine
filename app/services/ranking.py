class RankingService:

    def rank(self, candidates, features):

        quality_map = {
            feature.faiss_id: feature.quality_score
            for feature in features
        }

        scored = []

        if not candidates:
            return []

        best_similarity = candidates[0][1]

        if best_similarity < 0.26:
            return []

        similarity_threshold = (best_similarity - 0.05)

        for image_id, similarity in candidates:

            if similarity < similarity_threshold:
                continue

            quality_score = quality_map.get(image_id,0)


            final_score = (similarity + 0.01 * quality_score)


            scored.append(
                {
                    "id": image_id,
                    "score": final_score
                }
            )


        scored.sort(
            key=lambda x: x["score"],
            reverse=True
        )


        return [
            item["id"]
            for item in scored
        ]