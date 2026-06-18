from typing import List

import torch
torch.set_num_threads(1)

from PIL import Image
from transformers import CLIPProcessor, CLIPModel

from app.embeddings.base import EmbeddingProvider


class CLIPProvider(EmbeddingProvider):

    def __init__(self):
        self.model = CLIPModel.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

        self.processor = CLIPProcessor.from_pretrained(
            "openai/clip-vit-base-patch32"
        )

        self.model.eval()


    def encode_text(self, text: str) -> List[float]:
        print("START CLIP")
        inputs = self.processor(
            text=text,
            return_tensors="pt",
            padding=True
        )

        with torch.no_grad():

            outputs = self.model.text_model(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"]
            )
            embedding = outputs.pooler_output

            embedding = self.model.text_projection(embedding)
        print("END CLIP")
        return embedding[0].tolist()


    def encode_image(self, image_path: str) -> List[float]:

        image = Image.open(image_path)

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        with torch.no_grad():

            outputs = self.model.vision_model(
                pixel_values=inputs["pixel_values"]
            )

            embedding = outputs.pooler_output

            embedding = self.model.visual_projection(embedding)

        return embedding[0].tolist()