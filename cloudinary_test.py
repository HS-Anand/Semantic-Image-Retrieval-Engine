from app.storage.cloudinary_storage import CloudinaryStorage


storage = CloudinaryStorage()


url = storage.upload(
    "bird.jpeg"
)


print(url)