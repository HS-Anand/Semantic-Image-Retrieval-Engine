class RankingService:

    def rank(self, candidates, features):

        quality_map = {
            str(feature.id): feature.quality_score
            for feature in features
        }


        scored = []

        for candidate in candidates:

            image_id = candidate["id"]

            final_score = (
                0.85 * candidate["similarity"]
                +
                0.15 * quality_map[image_id]
            )

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