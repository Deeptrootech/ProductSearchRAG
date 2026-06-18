"""Simple FastAPI app."""
from fastapi import FastAPI, UploadFile, File
import shutil
import os
from services.FileProcess.file_processor import FileProcessor
from services.VectorDB.vector_store import VectorStore
from services.embedding_service import EmbeddingService
from services.intent_service import IntentService
from services.llm_service import LLMService
from services.utils import apply_filters, format_context, apply_sort

app = FastAPI()
vector_store = VectorStore()
llm_service = LLMService()
intent_service = IntentService()
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
    # # 1. INTENT extraction
    # print(f"=================== # 1. INTENT extraction")
    # intent, success = intent_service.extract_intent(user_query)
    # if not success:
    #     return intent
    # search_parts = [intent.get("search_text", "")]
    # if intent.get("brand"):
    #     search_parts.append(intent["brand"])
    # search_parts.extend(intent.get("required_features", []))
    # search_text = " ".join(p.strip() for p in search_parts if p)

    # 2. RETRIEVAL from vector database (Vector Search (semantic))
    print(f"=================== # 2. RETRIEVAL from vector database (overfetch!")
    retrieval_k = max(top_k * 50, 30)
    # products = vector_store.similarity_search_for_asked_question(search_text, top_k=retrieval_k)
    products = vector_store.similarity_search_for_asked_question(user_query, top_k=retrieval_k)
    print(f"++++++++++++++++++++ {products}")

    # # 3. FILTERING & SORTING
    # print(f"=================== # 3. FILTERING & SORTING")
    # products = apply_filters(products, intent)
    # products = apply_sort(products, intent)
    # Handle If no products filtered
    if not products:
        return {
            "products": [],
            "explanation": "No matching products found for given query."
        }

    # # 4. FORMAT
    # print(f"=================== # 4. FORMAT")
    # products = products[:top_k]
    # context = format_context(products)

    # 5. FINAL LLM RESPONSE
    print(f"=================== # 5. FINAL LLM RESPONSE")
    print(f"========ASKED TO LLM=========== {user_query} &&&&&&&&&&&&&&&&&&&&&&&&&&&&& {products}")
    final_response = llm_service.get_response(user_query, products)
    print(f"++++++++FINAL LLM RESPONSE+++++++++++++ {final_response}")
    return final_response
