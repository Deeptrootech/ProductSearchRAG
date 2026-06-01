"""
How it works:
    1. You send text → get a vector embedding
    2. Embeddings can then be inserted into vector DB (Milvus, Pinecone, Chroma, Weaviate etc.)
This replaces the need to run SentenceTransformers locally
"""

import requests

from .config import embedding_model, API_KEY, url


class EmbeddingService:

    def generate_embedding(self, text):
        try:
            response = requests.post(
                url,
                json={
                    "model": embedding_model,
                    "input": text
                },
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
            )
            if response.status_code != 200:
                print(f"Failed to generate embedding for text: {text} :: error: {response.json()}")
                return None

            return response.json()["data"][0]["embedding"]
        except Exception as e:
            print(f"Failed to generate embedding for text: {text} :: error: {str(e)}")
            return None
