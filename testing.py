from app.storage.cloudinary_storage import CloudinaryStorage


storage = CloudinaryStorage()


urls = storage.upload_many(
    [
        "/Users/harkarananand/Desktop/SIRE/sire-logo.png"
    ]
)


print(urls)