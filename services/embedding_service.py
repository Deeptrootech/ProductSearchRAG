"""
How it works:
    1. You send text → get a vector embedding
    2. Embeddings can then be inserted into vector DB (Milvus, Pinecone, Chroma, Weaviate etc.)
This OpenRouter API replaces the need to run SentenceTransformers locally
"""
import requests

from config import (
    EMBEDDING_URL,
    EMBEDDING_MODEL,
    OPENROUTER_API_KEY
)


class EmbeddingService:
    def get_embedding(self, text):
        try:
            response = requests.post(
                EMBEDDING_URL,
                json={
                    "model": EMBEDDING_MODEL,
                    "input": text
                },
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }
            )
            if response.status_code != 200:
                print("Error While Generating Embeddings", response.text)
                return None
            print(f"Embeddings Generated Successfully for: {text}")
            return response.json()["data"][0]["embedding"]
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None
