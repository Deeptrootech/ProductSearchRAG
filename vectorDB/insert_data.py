from openrouter.openrouter_for_embeddings import EmbeddingService
from vectorDB.vector_store import VectorStore

embedder = EmbeddingService()
vector_store = VectorStore()

final_products = []

from pymilvus import MilvusClient


class VectorStore:

    def __init__(self):
        self.client = MilvusClient(uri="http://localhost:19530")
        self.collection_name = "documents"

    def insert_products(self, products):
        data = []

        for product in products:
            data.append({
                "id": product["product_id"],
                "vector": product["embedding"],
                "product_name": product["product_name"],
                "category": product["category"],
                "price": product["price"],
                "features": product["features"],
                "description": product["description"],
            })

        self.client.insert(
            collection_name=self.collection_name,
            data=data
        )

    def generate_and_save_embeddings(self, products: list):
        for product in products:

            embedding = embedder.generate_embedding(
                product["combined_text"]
            )

            if embedding:
                product["embedding"] = embedding
                final_products.append(product)

        vector_store.insert_products(final_products)

        print("Products inserted successfully")
