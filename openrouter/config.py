import os

API_KEY = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/embeddings"

embedding_model = "nvidia/llama-nemotron-embed-vl-1b-v2:free"
vector_dimension = 384

llm_model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"  # openrouter/owl-alpha
