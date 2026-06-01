"""Simple FastAPI app."""
from fastapi import FastAPI, UploadFile, File
import shutil
import os

from services.FileProcess.file_processor import FileProcessor
from services.VectorDB.vector_store import VectorStore
from services.embedding_service import EmbeddingService
from services.llm_service import LLMService

app = FastAPI()
vector_store = VectorStore()
llm_service = LLMService()
file_processor = FileProcessor()
embedding_service = EmbeddingService()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Product Search API"}


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """Upload and process CSV file."""
    # Save file in upload directory
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Process & store products into vector databse with embeddings.
    products = file_processor.process_upload(file_path)
    vector_store.insert_products(products)

    return {"status": "success", "products_processed": len(products)}


@app.post("/search")
def search(query: str, top_k: int = 5):
    """
    Search products.
    This is a RAG (Retrieval Augmented Generation) system.
    """
    # Search from vector database
    products = vector_store.similarity_search_for_asked_question(query, top_k)

    # Get recommendation
    product_context = "\n".join([f"- {p['product_name']}: ${p['price']}" for p in products])
    recommendation = llm_service.get_response(query, product_context)

    return {
        "query": query,
        "products": products,
        "recommendation": recommendation,
        "total": len(products)
    }
