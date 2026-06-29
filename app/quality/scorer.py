import cv2


class ImageQualityScorer:


    def score(self, image_path: str) -> float:

        image = cv2.imread(image_path)
        

        if image is None:
            return 0.0

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

        if sharpness < 50:
            return 0.0

        return 1.0