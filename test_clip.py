from app.embeddings.clip_provider import CLIPProvider


provider = CLIPProvider()

vector = provider.encode_text("black hoodie")

print(type(vector))
print(len(vector))