"""Simple configuration file."""
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

# OpenRouter API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Embedding
EMBEDDING_URL = "https://openrouter.ai/api/v1/embeddings"
EMBEDDING_MODEL = "nvidia/llama-nemotron-embed-vl-1b-v2:free"

# Chat / LLM
LLM_URL = "https://openrouter.ai/api/v1/chat/completions"
LLM_MODEL = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"

# Milvus
MILVUS_URI = "http://localhost:19530"
DATABASE_NAME = "ProductSearchRAG"
COLLECTION_NAME = "products"
VECTOR_DIMENSION = 1024  # TODO: get this dynamically

# Search
TOP_K = 5
