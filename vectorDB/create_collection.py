from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType

# Connect to Milvus
connections.connect("default", host="localhost", port="19530")

# Define the schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="title", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=100),
    # Vector field: 384 dimensions (typical for sentence-transformers/all-MiniLM-L6-v2)
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
]

schema = CollectionSchema(fields, description="Document embeddings for semantic search")

# Create the collection
collection = Collection("documents", schema)

print(f"Collection created: {collection.name}")
print(f"Schema: {collection.schema}")
