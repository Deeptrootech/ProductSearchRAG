"""
************** architecture **************
Database
    ↓
Schema
    ↓
AUTOINDEX (COSINE)
    ↓
Collection
    ↓
Load Collection
    ↓
Insert Products
    ↓
Vector Search
"""
from pymilvus import MilvusClient, DataType

from config import MILVUS_URL, DATABASE_NAME, COLLECTION_NAME, TOP_K
from services.embedding_service import EmbeddingService


class VectorStore:
    """
    A proper production implementation should:
        - Create database
        - Create schema
        - Create index
        - Create collection using schema + index
        - Load collection
        - Batch insert embeddings
        - Search with HNSW + COSINE
    """

    def __init__(self):
        self.client = MilvusClient(uri=MILVUS_URL)
        self.embedding_service = EmbeddingService()
        # sample_embedding = self.embedding_service.get_embedding("test")
        self.vector_dimension = 2048

        self.setup()

    def setup(self):
        """
        Setup vector database, collection and index if missing.
        """
        # Create & use Database
        self.create_database()

        # --------------------------------------------------
        # Create schema design
        # --------------------------------------------------
        schema = self.create_schema_and_add_fields()

        # --------------------------------------------------
        # Create schema index
        # --------------------------------------------------
        index_params = self.create_index()

        # --------------------------------------------------
        # Create collection
        # --------------------------------------------------
        self.create_collection(schema, index_params)
        self.load_collection()

    def create_database(self):
        databases = self.client.list_databases()

        if DATABASE_NAME not in databases:
            self.client.create_database(DATABASE_NAME)
            print("## New Milvus DB created")
        else:
            print("## DB already exists")
        self.client.use_database(DATABASE_NAME)

    def create_collection(self, schema, index_params):
        if self.client.has_collection(COLLECTION_NAME):
            print("## collection Already Exists:")
            return
        else:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                schema=schema,
                index_params=index_params,
            )
            print(f"Collection '{COLLECTION_NAME}' created successfully.")

    def load_collection(self):
        try:
            self.client.load_collection(COLLECTION_NAME)
            print(f"Collection '{COLLECTION_NAME}' loaded.")
        except Exception as e:
            print(f"Load collection failed: {e}")

    def create_schema_and_add_fields(self):
        schema = self.client.create_schema(
            auto_id=True,
            enable_dynamic_field=False,
        )

        schema.add_field(
            field_name="id",
            datatype=DataType.INT64,
            is_primary=True,
        )

        schema.add_field(
            field_name="vector",
            datatype=DataType.FLOAT_VECTOR,
            dim=self.vector_dimension,
        )

        schema.add_field(
            field_name="product_id",
            datatype=DataType.VARCHAR,
            max_length=100,
        )

        schema.add_field(
            field_name="product_name",
            datatype=DataType.VARCHAR,
            max_length=500,
        )

        schema.add_field(
            field_name="brand",
            datatype=DataType.VARCHAR,
            max_length=200,
        )

        schema.add_field(
            field_name="category",
            datatype=DataType.VARCHAR,
            max_length=200,
        )

        schema.add_field(
            field_name="price",
            datatype=DataType.FLOAT,
        )

        schema.add_field(
            field_name="rating",
            datatype=DataType.FLOAT,
        )

        schema.add_field(
            field_name="stock",
            datatype=DataType.INT64,
        )

        schema.add_field(
            field_name="features",
            datatype=DataType.VARCHAR,
            max_length=5000,
        )

        schema.add_field(
            field_name="description",
            datatype=DataType.VARCHAR,
            max_length=10000,
        )

        schema.add_field(
            field_name="combined_text",
            datatype=DataType.VARCHAR,
            max_length=4000,
        )

        return schema

    def create_index(self):
        index_params = self.client.prepare_index_params()

        index_params.add_index(
            field_name="vector",
            metric_type="COSINE",
            index_type="AUTOINDEX",
        )

        return index_params

    def insert_products(self, products):
        """
        Generate embeddings of each raw and insert into database along with metadata.
        """

        data = []
        for product in products:
            try:
                embedding = self.embedding_service.get_embedding(product["combined_text"])

                if embedding:
                    data.append({
                        "product_id": str(product.get("product_id")),
                        "product_name": product.get("product_name", ""),
                        "brand": product.get("brand", ""),
                        "category": product.get("category", ""),
                        "price": float(product.get("price", 0)),
                        "rating": float(product.get("rating", 0)),
                        "stock": int(product.get("stock", 0)),
                        "features": product.get("features", ""),
                        "description": product.get("description", ""),
                        "combined_text": product.get("combined_text", ""),
                        "vector": embedding,
                    })
            except Exception as e:
                print(f"Embedding failed for {product.get('product_id')}: {e}")
        if not data:
            print("No products found")
            return

        self.client.insert(collection_name=COLLECTION_NAME, data=data)

    def similarity_search_for_asked_question(self, query, filter_expr=None, top_k=TOP_K):
        """
        Search for similar embeddings from vector db and return top-k results.
        """
        try:
            query_embedding = self.embedding_service.get_embedding(query)
            if not query_embedding:
                return {"error": "Failed to get embedding"}

            results = self.client.search(
                collection_name=COLLECTION_NAME,
                data=[query_embedding],
                anns_field="vector",
                filter=filter_expr,
                # Approximate Nearest Neighbor Search -> tells Milvus which vector field to search against.
                search_params={
                    "metric_type": "COSINE",
                },
                limit=top_k,
                output_fields=[
                    "product_id",
                    "product_name",
                    "category",
                    "price",
                    "rating",
                    "stock",
                    "brand",
                    "features",
                    "description",
                    "combined_text"
                ]
            )

            products = []
            for result in results[0]:
                entity = result.get("entity", {})
                products.append(
                    {
                        "product_id": entity.get("product_id"),
                        "product_name": entity.get("product_name"),
                        "category": entity.get("category"),
                        "price": entity.get("price"),
                        "rating": entity.get("rating"),
                        "stock": entity.get("stock"),
                        "brand": entity.get("brand"),
                        "features": entity.get("features"),
                        "description": entity.get("description"),
                        "combined_text": entity.get("combined_text"),
                        "score": result.get("distance"),
                    }
                )

            return products
        except Exception as e:
            print(f"Error in similarity search: {str(e)}")
            return []
