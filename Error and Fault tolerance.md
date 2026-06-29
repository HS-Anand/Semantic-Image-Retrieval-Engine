Offline batch processing->

1. data folder/directory not found/exist
2. there are no images in the found dir/folder
3. Unsupported image files extensions skipped
4. Corrupt image detection and handling
5. Cloudinary failed to upload image handles
6. PostgreSQL roll back
7. FAISS index save failure handled


Online query retreivel->

1. Empty query
2. FAISS index missing
3. Search service failure, including repository/databse, CLIP encoding error, FAISS search failure, ranking failure, hydration failure
4. Invalid pagination
