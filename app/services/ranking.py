class RankingService:

    def rank(self, candidates, features):

        quality_map = {
            feature.faiss_id: feature.quality_score
            for feature in features
        }


        scored = []


        for image_id, similarity in candidates:

            quality_score = quality_map.get(image_id, 0)


            final_score = (0.975 * similarity + 0.025 * quality_score)


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