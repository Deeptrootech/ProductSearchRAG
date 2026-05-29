from pymilvus import MilvusClient

# *********************** Step 1: Connect to Milvus ***********************
client = MilvusClient(uri="http://localhost:19530")

# *********************** Step 2: Create database ***********************
db_name = "ProductSearchRAG"
if db_name not in client.list_databases():
    client.create_database(db_name)
    print("DB created")
else:
    print("DB already exists")

# *********************** Step 3: Create collection ***********************
COLLECTION_NAME = "documents"
DIMENSION = 1024  # replace with your real embedding dim

# Check if collection exists
if client.has_collection(COLLECTION_NAME):
    info = client.describe_collection(COLLECTION_NAME)
    print("collection Already Exists:", info)
else:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        dimension=DIMENSION,
        metric_type="L2"
    )
    print(f"Collection '{COLLECTION_NAME}' created successfully.")
