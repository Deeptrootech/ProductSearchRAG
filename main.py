"""Simple FastAPI app."""
from fastapi import FastAPI, UploadFile, File
import shutil
import os
from services.FileProcess.file_processor import FileProcessor
from services.VectorDB.vector_store import VectorStore
from services.embedding_service import EmbeddingService
from services.intent_service import IntentService
from services.llm_service import LLMService
from services.ranking_service import RankingService
from services.utils import apply_filters, format_context

app = FastAPI()
vector_store = VectorStore()
llm_service = LLMService()
intent_service = IntentService()
ranking_service = RankingService()
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

    # Process & store products into vector database with embeddings.
    products = file_processor.process_upload(file_path)
    vector_store.insert_products(products)

    return {"status": "success", "products_processed": len(products)}


@app.post("/search")
def search(user_query: str, top_k: int = 5):
    """
    Search products.
    This is a RAG (Retrieval Augmented Generation) system.
    """
    # 1. INTENT (safe extraction, NOT strict)
    print(f"=================== # 1. INTENT (safe extraction, NOT strict)")
    intent, success = intent_service.extract_intent(user_query)
    if not success:
        return intent
    search_text = intent["search_text"]
    # light query enrichment
    if intent.get("brand"):
        search_text += " " + intent["brand"]

    if intent.get("required_features"):
        search_text += " " + " ".join(intent["required_features"])

    # 2. RETRIEVAL from vector database (overfetch!)
    print(f"=================== # 2. RETRIEVAL from vector database (overfetch!")
    products = vector_store.similarity_search_for_asked_question(search_text, top_k=50)

    # 3. FILTERING (deterministic)
    print(f"=================== # 3. FILTERING (deterministic)")
    candidates = apply_filters(products, intent)

    # 4. RANKING (hybrid scoring)
    print(f"=================== # 4. RANKING (hybrid scoring)")
    candidates = ranking_service.rank(candidates, intent)

    # 5. LIMIT
    candidates = candidates[:top_k]

    # 6. FORMAT
    print(f"=================== # 6. FORMAT")
    context = format_context(candidates)

    print(f"=================== {candidates}")
    # 7. FINAL LLM RESPONSE
    print(f"=================== # 7. FINAL LLM RESPONSE")
    reccomandation = llm_service.get_response(user_query, context)
    print(f"+++++++++++++++++++++ {candidates}")

    return reccomandation
