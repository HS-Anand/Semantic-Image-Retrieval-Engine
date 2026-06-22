import os
import random
import shutil


SOURCE_FOLDER = "/Users/harkarananand/Desktop/data_pattern/tribal"
TARGET_FOLDER = "/Users/harkarananand/Desktop/SIRE/dataset"

SAMPLE_SIZE = 20


os.makedirs(
    TARGET_FOLDER,
    exist_ok=True
)


images = [
    file
    for file in os.listdir(SOURCE_FOLDER)
    if file.lower().endswith(
        (
            ".jpg",
            ".jpeg",
            ".png"
        )
    )
]


selected = random.sample(
    images,
    SAMPLE_SIZE
)


for image in selected:

    shutil.copy(
        os.path.join(
            SOURCE_FOLDER,
            image
        ),

        os.path.join(
            TARGET_FOLDER,
            image
        )
    )


print(
    f"Copied {len(selected)} images"
)