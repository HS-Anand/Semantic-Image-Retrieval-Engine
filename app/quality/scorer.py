import cv2


class ImageQualityScorer:


    def score(self, image_path: str) -> float:

        image = cv2.imread(image_path)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        variance = cv2.Laplacian(gray, cv2.CV_64F).var()

        normalized_score = min(variance / 1000, 1.0)

        return normalized_score