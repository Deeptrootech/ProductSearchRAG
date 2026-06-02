from pymilvus import MilvusClient

from config import MILVUS_URL, DATABASE_NAME, COLLECTION_NAME, VECTOR_DIMENSION, TOP_K

from services.embedding_service import EmbeddingService


class VectorStore:

    def __init__(self):
        self.client = MilvusClient(uri=MILVUS_URL)
        self.embedding_service = EmbeddingService()
        sample_embedding = self.embedding_service.get_embedding("test")
        self.vector_dimension = len(sample_embedding)
        self.setup()

    def setup(self):
        """
        Setup vector databse and collection.
        """
        # *********************** Create database ***********************
        if DATABASE_NAME not in self.client.list_databases():
            self.client.create_database(DATABASE_NAME)
            print("## New Milvus DB created")
        else:
            print("## DB already exists")

        self.client.use_database(DATABASE_NAME)

        # *********************** Create collection ***********************
        if self.client.has_collection(COLLECTION_NAME):
            info = self.client.describe_collection(COLLECTION_NAME)
            print("## collection Already Exists:", info)
        else:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                dimension=self.vector_dimension,
                metric_type="L2",
                auto_id=True,
                enable_dynamic_field=True
            )
            print(f"## Collection '{COLLECTION_NAME}' created successfully.")

    def insert_products(self, products):
        """
        Genarate embeddings of each raw and insert into database along with metadata.
        """

        data = []
        for product in products:
            embedding = self.embedding_service.get_embedding(product["combined_text"])

            if embedding:
                data.append({
                    "vector": embedding,
                    "product_id": product.get("product_id"),
                    "product_name": product.get("product_name", ""),
                    "category": product.get("category", ""),
                    "price": product.get("price", 0),
                    "features": product.get("features", ""),
                    "description": product.get("description", ""),
                })

        if not data:
            print("No products found")
            return

        self.client.insert(collection_name=COLLECTION_NAME, data=data)

    def similarity_search_for_asked_question(self, query, top_k=TOP_K):
        """
        Search for similar embeddings from vector db and return top-k results.
        """
        query_embedding = self.embedding_service.get_embedding(query)
        if not query_embedding:
            return {"error": "Failed to get embedding"}

        results = self.client.search(
            collection_name=COLLECTION_NAME,
            data=[query_embedding],
            limit=top_k,
            output_fields=[
                "product_id",
                "product_name",
                "category",
                "price",
                "features",
                "description"
            ]
        )

        products = []
        for result in results[0]:
            entity = result["entity"]

            products.append({
                "product_id": entity["product_id"],
                "product_name": entity["product_name"],
                "category": entity["category"],
                "price": entity["price"],
                "features": entity["features"],
                "description": entity["description"],
                "score": result["distance"]
            })

        return products
