Testing via custom file while side-by-side development

1. clip testing test_clip.py
2. temporrary faiss index to check faiss searching create_test_index.py
3. test_faiss.py
4. test_quality.py to test opencv quality scoring
5. app.config works test
6. cloudinary upload and url test
7. tested batch clipping and batch faiss generation
8. tested batch insertion in both postgresql and then cloudinary with 8 workers, threads